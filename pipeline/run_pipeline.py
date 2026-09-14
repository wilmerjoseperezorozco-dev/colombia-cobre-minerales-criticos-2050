"""
Orquestador del pipeline completo — ejecuta las 4 fases en orden y detiene
la cadena si una fase crítica falla (fail-fast), salvo la Fase 3, que es
best-effort por naturaleza (depende de páginas HTML de terceros sin API).

Uso:
    python pipeline/run_pipeline.py

Fases:
    1. phase1_seed              — valida el dataset curado a mano (bloqueante)
    2. phase2_live_fetch        — precio de cobre en vivo desde FRED (bloqueante)
    3. phase3_scrape_oficiales  — snapshot de fuentes oficiales colombianas (no bloqueante)
    4. phase4_consolidacion     — arma el dataset_maestro.json final (bloqueante)
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
    ("Fase 4 — Consolidación del dataset maestro", "phase4_consolidacion/build_dataset_maestro.py", True),
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
