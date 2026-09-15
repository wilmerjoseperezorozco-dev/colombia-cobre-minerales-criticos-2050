"""
AUDITORÍA SEMANAL — archiva `dataset_maestro.json` con numeración ISO de
semana y lo compara contra el snapshot archivado más reciente (agregado
15-sep-2026, en respuesta a la pregunta: "¿cómo se comparan los cambios
semanales del dataset_maestro.json? ¿se guarda historial o se sobrescribe
cada vez?" — antes de esto, la respuesta honesta era "se sobrescribe: no
hay historial, y un cambio anómalo en una fuente pasaría desapercibido").

Qué hace:
  1. Compara el dataset_maestro.json actual contra el snapshot archivado más
     reciente (si existe) en un conjunto curado de CAMPOS_CLAVE numéricos.
  2. Calcula variación porcentual por campo y marca ALERTA si supera
     UMBRAL_ALERTA_PCT (ej. un precio que cae más de 50% de una semana a
     otra probablemente sea un error de la fuente, no un movimiento real
     de mercado -- ver docs/ADR_002 sobre por qué el precio viene de FRED).
  3. Escribe el reporte en `data/consolidado/_audit_semana_<AAAA>_W<SS>.json`.
  4. Archiva una copia del dataset actual en
     `data/consolidado/historico/dataset_maestro_<AAAA>_W<SS>.json`.

Qué NO hace (limitación reconocida, igual que el resto del pipeline):
  - No compara el JSON completo campo por campo -- eso generaría ruido
    constante (fechas de "actualizado", notas metodológicas que cambian de
    redacción sin cambiar de dato). Compara solo los campos numéricos que
    de verdad importan para detectar un problema de fuente.
  - No bloquea el pipeline si detecta una alerta -- esto es un guardrail de
    OBSERVABILIDAD, no de validación dura como
    `pipeline/validaciones/validar_dataset_maestro.py`. Una alerta se
    reporta, no impide que el pipeline termine (una caída de precio real y
    fuerte SÍ puede pasar; queremos que quede señalada para revisión
    humana, no que tumbe el pipeline).
  - Es no bloqueante por diseño: en la primera corrida (sin historial
    todavía) no hay nada que comparar -- se archiva y se sigue, sin error.

Uso:
    python pipeline/auditoria_semanal/comparar_dataset_maestro.py
"""
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[2]
DATASET_MAESTRO_PATH = REPO_ROOT / "data" / "consolidado" / "dataset_maestro.json"
HISTORICO_DIR = REPO_ROOT / "data" / "consolidado" / "historico"
AUDIT_DIR = REPO_ROOT / "data" / "consolidado"

UMBRAL_ALERTA_PCT = 50.0


def _obtener(d, *claves):
    """Navega un dict anidado por una ruta de claves; retorna None si
    cualquier tramo del camino no existe, en vez de lanzar KeyError -- un
    dataset viejo (de antes de que existiera un campo) es un caso normal a
    manejar, no un error."""
    for clave in claves:
        if not isinstance(d, dict):
            return None
        d = d.get(clave)
    return d


def _ultimo_precio_cobre(dataset: dict):
    serie = _obtener(dataset, "bloques", "precio_cobre_serie_historica", "datos", "serie_completa")
    if not serie:
        return None
    return serie[-1].get("precio_usd_por_tonelada")


# Campos numéricos curados a mano -- no todo el JSON, solo lo que de verdad
# importaría si cambiara de golpe (ver docstring del módulo).
CAMPOS_CLAVE = [
    ("precio_cobre_ultimo_valor_usd_por_tonelada", _ultimo_precio_cobre),
    ("precio_cobre_cagr_5_anos_pct",
     lambda ds: _obtener(ds, "bloques", "precio_cobre_serie_historica", "metricas_calculadas", "cagr_5_anos_pct")),
    ("potencial_colombia_total_mt_cu",
     lambda ds: _obtener(ds, "bloques", "potencial_colombia_y_retos", "datos", "potencial_geologico",
                          "potencial_colombia_propio_total_mt_cu")),
    ("iea_demanda_mundial_2025_linea_base_kt",
     lambda ds: _obtener(ds, "bloques", "demanda_global_cobre", "datos", "demanda_total_cobre_iea_2026_kt",
                          "2025_linea_base")),
    ("usgs_pct_potencial_colombia_sobre_reservas_mundiales",
     lambda ds: _obtener(ds, "bloques", "usgs_mineral_commodity_summaries_copper", "datos",
                          "contexto_colombia_vs_usgs", "pct_potencial_colombia_sobre_reservas_mundiales")),
]


def comparar_valores_clave(actual: dict, previo: dict) -> dict:
    """Función pura: compara CAMPOS_CLAVE entre dos dataset_maestro.json
    (sin tocar disco) y retorna {"campos": [...], "alertas": [...]}.
    Separada de main() para poder testear la lógica de detección de
    anomalías con fixtures sintéticos, sin necesitar dos archivos reales
    archivados en disco."""
    campos = []
    alertas = []
    for etiqueta, extractor in CAMPOS_CLAVE:
        v_actual = extractor(actual)
        v_previo = extractor(previo)
        variacion_pct = None
        if isinstance(v_actual, (int, float)) and isinstance(v_previo, (int, float)) and v_previo != 0:
            variacion_pct = round((v_actual - v_previo) / abs(v_previo) * 100, 2)
        campos.append({
            "campo": etiqueta, "valor_previo": v_previo, "valor_actual": v_actual,
            "variacion_pct": variacion_pct,
        })
        if variacion_pct is not None and abs(variacion_pct) > UMBRAL_ALERTA_PCT:
            alertas.append(
                f"{etiqueta}: cambió {variacion_pct}% ({v_previo} -> {v_actual}), "
                f"supera el umbral de {UMBRAL_ALERTA_PCT}%"
            )
    return {"campos": campos, "alertas": alertas}


def _semana_iso_actual() -> tuple[int, int]:
    anio, semana, _ = datetime.now(timezone.utc).isocalendar()
    return anio, semana


def main() -> int:
    if not DATASET_MAESTRO_PATH.exists():
        print(f"No existe {DATASET_MAESTRO_PATH} -- ¿corrió la Fase 4 antes que esta auditoría?")
        return 1  # el orquestador la trata como no bloqueante de todos modos

    HISTORICO_DIR.mkdir(parents=True, exist_ok=True)
    anio, semana = _semana_iso_actual()
    etiqueta_semana = f"{anio}_W{semana:02d}"
    ruta_snapshot_actual = HISTORICO_DIR / f"dataset_maestro_{etiqueta_semana}.json"

    with open(DATASET_MAESTRO_PATH, "r", encoding="utf-8") as f:
        dataset_actual = json.load(f)

    snapshots_previos = sorted(
        p for p in HISTORICO_DIR.glob("dataset_maestro_*.json") if p != ruta_snapshot_actual
    )

    if not snapshots_previos:
        print(
            "Sin snapshot previo archivado -- primera corrida de la auditoría semanal "
            "(o primera vez que corre esta semana ISO). Se archiva sin comparar."
        )
        shutil.copy(DATASET_MAESTRO_PATH, ruta_snapshot_actual)
        print(f"Snapshot archivado en: {ruta_snapshot_actual}")
        return 0

    ruta_previo = snapshots_previos[-1]
    with open(ruta_previo, "r", encoding="utf-8") as f:
        dataset_previo = json.load(f)

    comparacion = comparar_valores_clave(dataset_actual, dataset_previo)
    reporte = {
        "generado_utc": datetime.now(timezone.utc).isoformat(),
        "semana_actual": etiqueta_semana,
        "comparado_contra": ruta_previo.name,
        **comparacion,
    }

    ruta_reporte = AUDIT_DIR / f"_audit_semana_{etiqueta_semana}.json"
    with open(ruta_reporte, "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)

    # Archivar el snapshot actual DESPUÉS de leer el previo -- si algo falla
    # arriba, no queremos haber sobrescrito el punto de comparación.
    shutil.copy(DATASET_MAESTRO_PATH, ruta_snapshot_actual)

    print(f"Comparado contra: {ruta_previo.name}")
    print(f"Reporte guardado en: {ruta_reporte}")
    if comparacion["alertas"]:
        print(f"\n{len(comparacion['alertas'])} ALERTA(S):")
        for alerta in comparacion["alertas"]:
            print(f"  ⚠ {alerta}")
    else:
        print("Sin anomalías -- ningún campo clave superó el umbral de "
              f"{UMBRAL_ALERTA_PCT}% de variación.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
