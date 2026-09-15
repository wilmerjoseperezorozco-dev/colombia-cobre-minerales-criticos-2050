"""
Orquestador del pipeline completo — ejecuta las 4 fases en orden y detiene
la cadena si una fase crítica falla (fail-fast), salvo la Fase 3, que es
best-effort por naturaleza (depende de páginas HTML de terceros sin API).

Uso:
    python pipeline/run_pipeline.py

Fases (el número de carpeta indica el orden en que se agregaron al pipeline,
no el orden de ejecución — la consolidación (4) siempre corre al final para
poder incluir todo lo que las demás fases produjeron, incluida la 5):
    1. phase1_seed              — valida el dataset curado a mano (bloqueante)
    2. phase2_live_fetch        — precio de cobre en vivo desde FRED (bloqueante)
    3. phase3_scrape_oficiales  — snapshot de fuentes oficiales colombianas (no bloqueante)
    5. phase5_usgs              — USGS Mineral Commodity Summaries, ficha de Copper (no bloqueante)
    6. phase6_iea               — ingesta manual del IEA Critical Minerals Data Explorer (no bloqueante)
    7. phase7_upme_sgc          — informe técnico UPME: recursos/reservas por proyecto (no bloqueante)
    8. phase8_usgs_historia     — serie histórica de cobre en EE.UU. desde 1900 (no bloqueante)
    9. phase9_upme_auditoria    — catálogo de tablas de los 2 PDFs de UPME restantes + PIB minero regional (no bloqueante)
    4. phase4_consolidacion     — arma el dataset_maestro.json final (bloqueante)
    G. validaciones             — guardrail de consistencia lógica sobre el dataset final (bloqueante, corre último)
"""
import os
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
PIPELINE_DIR = REPO_ROOT / "pipeline"
ENV_UTF8 = {**os.environ, "PYTHONIOENCODING": "utf-8"}

FASES = [
    ("Fase 1 — Validación del dataset semilla", "phase1_seed/validate_seed.py", True),
    ("Fase 2 — Precio de cobre en vivo (FRED)", "phase2_live_fetch/fetch_copper_price_fred.py", True),
    ("Fase 3 — Snapshot de fuentes oficiales colombianas", "phase3_scrape_oficiales/fetch_fuentes_colombianas.py", False),
    ("Fase 5 — USGS Mineral Commodity Summaries (Copper)", "phase5_usgs/fetch_usgs_copper_mcs.py", False),
    ("Fase 6 — IEA Critical Minerals Data Explorer (ingesta manual)", "phase6_iea/ingest_iea_manual.py", False),
    ("Fase 7 — Informe técnico UPME (recursos/reservas por proyecto)", "phase7_upme_sgc/fetch_upme_informe_cobre.py", False),
    ("Fase 8 — Serie histórica de cobre en EE.UU. desde 1900 (USGS DS140)", "phase8_usgs_historia/fetch_usgs_ds140_copper.py", False),
    ("Fase 9 — Auditoría de los 2 PDFs de UPME restantes", "phase9_upme_auditoria/audit_upme_docs_adicionales.py", False),
    ("Fase 4 — Consolidación del dataset maestro", "phase4_consolidacion/build_dataset_maestro.py", True),
    ("Guardrail — Validación de consistencia lógica", "validaciones/validar_dataset_maestro.py", True),
]


def ejecutar(nombre, script_relativo, bloqueante):
    print(f"\n{'=' * 70}\n{nombre}\n{'=' * 70}")
    inicio = time.time()
    resultado = subprocess.run([sys.executable, str(PIPELINE_DIR / script_relativo)], env=ENV_UTF8)
    duracion = round(time.time() - inicio, 2)
    ok = resultado.returncode == 0
    print(f"[{'OK' if ok else 'FALLÓ'}] {nombre} ({duracion}s)")
    if not ok and bloqueante:
        print(f"\nPipeline detenido: '{nombre}' es una fase bloqueante y falló.")
        sys.exit(resultado.returncode)
    return ok


def main():
    print("Pipeline de datos — Cobre y minerales críticos en Colombia")
    resumen = []
    for nombre, script, bloqueante in FASES:
        ok = ejecutar(nombre, script, bloqueante)
        resumen.append((nombre, ok))

    print(f"\n{'=' * 70}\nRESUMEN\n{'=' * 70}")
    for nombre, ok in resumen:
        print(f"  [{'OK' if ok else 'FALLÓ (no bloqueante)'}] {nombre}")
    print("\nDataset maestro disponible en: data/consolidado/dataset_maestro.json")


if __name__ == "__main__":
    main()
