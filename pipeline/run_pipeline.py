"""
Orquestador del pipeline completo — ejecuta las fases y detiene la cadena
si una fase crítica (bloqueante) falla (fail-fast), salvo las fases
no bloqueantes, que son best-effort por naturaleza (dependen de fuentes de
terceros sin API, o de un parseo de PDF que podría romperse en una edición
futura del documento).

Uso:
    python pipeline/run_pipeline.py

Fases (el número de carpeta indica el orden en que se agregaron al pipeline,
no el orden de ejecución):
    1. phase1_seed              — valida el dataset curado a mano (bloqueante, secuencial)
    2. phase2_live_fetch        — precio de cobre en vivo desde FRED (bloqueante, secuencial)
    3. phase3_scrape_oficiales  — snapshot de fuentes oficiales colombianas (no bloqueante)
    5. phase5_usgs              — USGS Mineral Commodity Summaries, ficha de Copper (no bloqueante)
    6. phase6_iea               — ingesta manual del IEA Critical Minerals Data Explorer (no bloqueante)
    7. phase7_upme_sgc          — informe técnico UPME: recursos/reservas por proyecto (no bloqueante)
    8. phase8_usgs_historia     — serie histórica de cobre en EE.UU. desde 1900 (no bloqueante)
    9. phase9_upme_auditoria    — catálogo de tablas de los 2 PDFs de UPME restantes + PIB minero regional (no bloqueante)
    4. phase4_consolidacion     — arma el dataset_maestro.json final (bloqueante, secuencial)
    A. auditoria_semanal        — archiva el dataset y compara contra la semana anterior (no bloqueante)
    G. validaciones             — guardrail de consistencia lógica sobre el dataset final (bloqueante, secuencial)

Paralelización (agregado 15-sep-2026, respuesta a "¿qué pasa si se agregan
las fases 10-15?"): las fases 3/5/6/7/8/9 son independientes entre sí — cada
una lee sus propias fuentes y escribe su propio archivo en data/live/, sin
leer lo que escriben las demás. Por eso corren en paralelo vía
ThreadPoolExecutor, con un tope de hilos (no ilimitado: evita saturar de
golpe las fuentes externas con 6+ requests simultáneas). Fase 4 espera a que
TODAS terminen antes de consolidar — no puede arrancar antes, porque lee los
archivos que las fases 3/5-9 producen. 1, 2, 4 y el guardrail siguen
secuenciales porque son bloqueantes por diseño: si 1 o 2 fallan, no tiene
sentido seguir; 4 y el guardrail dependen de que todo lo anterior ya existe.

Nota para cuando esto deje de alcanzar (ver docs/09-metodologia-pipeline.md,
sección de roadmap): un ThreadPoolExecutor plano no da reintentos por fase
completa, backfill histórico, ni un grafo de dependencias declarativo más
fino que "bloqueante/no bloqueante". Si el pipeline crece a 15+ fases con
dependencias cruzadas reales entre ellas (no solo "todas antes de la 4"),
ese es el punto de migrar a Airflow o Prefect — no antes, sería complejidad
sin necesidad real todavía.
"""
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
from pipeline.logging_utils import Cronometro, RegistroEjecucion, configurar_logging  # noqa: E402

PIPELINE_DIR = REPO_ROOT / "pipeline"
ENV_UTF8 = {**os.environ, "PYTHONIOENCODING": "utf-8"}

logger = configurar_logging()

# Máximo de fases no bloqueantes corriendo a la vez. No es "todas al mismo
# tiempo" a propósito -- varias de estas le pegan a la misma familia de
# dominios (usgs.gov, upme.gov.co) y lanzar 6 requests de golpe es más
# probable que dispare un límite de tasa que ahorrar tiempo real.
MAX_HILOS_NO_BLOQUEANTES = 3

FASES_SECUENCIALES_INICIALES = [
    ("Fase 1 — Validación del dataset semilla", "phase1_seed/validate_seed.py"),
    ("Fase 2 — Precio de cobre en vivo (FRED)", "phase2_live_fetch/fetch_copper_price_fred.py"),
]

FASES_PARALELAS_NO_BLOQUEANTES = [
    ("Fase 3 — Snapshot de fuentes oficiales colombianas", "phase3_scrape_oficiales/fetch_fuentes_colombianas.py"),
    ("Fase 5 — USGS Mineral Commodity Summaries (Copper)", "phase5_usgs/fetch_usgs_copper_mcs.py"),
    ("Fase 6 — IEA Critical Minerals Data Explorer (ingesta manual)", "phase6_iea/ingest_iea_manual.py"),
    ("Fase 7 — Informe técnico UPME (recursos/reservas por proyecto)", "phase7_upme_sgc/fetch_upme_informe_cobre.py"),
    ("Fase 8 — Serie histórica de cobre en EE.UU. desde 1900 (USGS DS140)", "phase8_usgs_historia/fetch_usgs_ds140_copper.py"),
    ("Fase 9 — Auditoría de los 2 PDFs de UPME restantes", "phase9_upme_auditoria/audit_upme_docs_adicionales.py"),
]

FASES_SECUENCIALES_FINALES = [
    ("Fase 4 — Consolidación del dataset maestro", "phase4_consolidacion/build_dataset_maestro.py", True),
    ("Auditoría semanal — archivo + comparación histórica", "auditoria_semanal/comparar_dataset_maestro.py", False),
    ("Guardrail — Validación de consistencia lógica", "validaciones/validar_dataset_maestro.py", True),
]


def ejecutar(nombre: str, script_relativo: str, registro: RegistroEjecucion) -> bool:
    """Corre una fase como subproceso aislado (así un crash de pdfplumber o
    pandas en una fase no tumba el proceso del orquestador ni contamina el
    estado de las demás) y registra su resultado y duración."""
    logger.info("Iniciando: %s", nombre)
    with Cronometro() as cronometro:
        resultado = subprocess.run(
            [sys.executable, str(PIPELINE_DIR / script_relativo)], env=ENV_UTF8
        )
    ok = resultado.returncode == 0
    excepcion = None
    if not ok:
        excepcion = RuntimeError(
            f"'{script_relativo}' terminó con código de salida {resultado.returncode}"
        )
    registro.registrar(
        fase=nombre, estado="ok" if ok else "fallo",
        duracion_s=cronometro.duracion_s, excepcion=excepcion,
    )
    nivel_log = logger.info if ok else logger.error
    nivel_log("[%s] %s (%.2fs)", "OK" if ok else "FALLÓ", nombre, cronometro.duracion_s)
    return ok


def ejecutar_bloqueante(nombre: str, script_relativo: str, registro: RegistroEjecucion):
    """Para las fases que detienen el pipeline si fallan (1, 2, 4, guardrail):
    corre, registra, y si falla, guarda el log de ejecución ANTES de salir
    -- para que una corrida de CI que aborta a mitad de camino deje
    evidencia de hasta dónde llegó, no solo el código de salida genérico."""
    ok = ejecutar(nombre, script_relativo, registro)
    if not ok:
        registro.guardar()
        logger.error("Pipeline detenido: '%s' es una fase bloqueante y falló.", nombre)
        sys.exit(1)


def ejecutar_fases_paralelas(fases: list, registro: RegistroEjecucion) -> list:
    """Corre las fases no bloqueantes independientes entre sí en paralelo.
    Cada una escribe su propio archivo en data/live/ y no depende de lo que
    escriben las demás -- por eso es seguro paralelizarlas."""
    resultados = []
    with ThreadPoolExecutor(max_workers=MAX_HILOS_NO_BLOQUEANTES) as executor:
        futuros = {
            executor.submit(ejecutar, nombre, script, registro): nombre
            for nombre, script in fases
        }
        for futuro in as_completed(futuros):
            nombre = futuros[futuro]
            try:
                resultados.append((nombre, futuro.result()))
            except Exception as e:  # noqa: BLE001 -- fase no bloqueante: se registra, no se propaga
                logger.error("Excepción inesperada en '%s': %s", nombre, e)
                registro.registrar(fase=nombre, estado="fallo", duracion_s=0.0, excepcion=e)
                resultados.append((nombre, False))
    return resultados


def main():
    logger.info("Pipeline de datos — Cobre y minerales críticos en Colombia")
    registro = RegistroEjecucion()
    resumen = []

    for nombre, script in FASES_SECUENCIALES_INICIALES:
        ejecutar_bloqueante(nombre, script, registro)
        resumen.append((nombre, True))

    logger.info(
        "Lanzando %d fases no bloqueantes en paralelo (máx %d hilos a la vez)",
        len(FASES_PARALELAS_NO_BLOQUEANTES), MAX_HILOS_NO_BLOQUEANTES,
    )
    resumen.extend(ejecutar_fases_paralelas(FASES_PARALELAS_NO_BLOQUEANTES, registro))

    for nombre, script, bloqueante in FASES_SECUENCIALES_FINALES:
        if bloqueante:
            ejecutar_bloqueante(nombre, script, registro)
            resumen.append((nombre, True))
        else:
            resumen.append((nombre, ejecutar(nombre, script, registro)))

    ruta_log = registro.guardar()
    logger.info("Log de ejecución guardado en: %s", ruta_log)

    logger.info("=" * 70)
    logger.info("RESUMEN")
    for nombre, ok in resumen:
        logger.info("  [%s] %s", "OK" if ok else "FALLÓ (no bloqueante)", nombre)
    logger.info("Dataset maestro disponible en: data/consolidado/dataset_maestro.json")


if __name__ == "__main__":
    main()
