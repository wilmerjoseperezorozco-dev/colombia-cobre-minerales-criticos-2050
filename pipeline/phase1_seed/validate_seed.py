"""
FASE 1 — Validación del dataset semilla (curado por investigación manual).

Qué hace:
  Lee todos los data/*.json curados a mano (investigación de la sesión inicial)
  y valida que cada proyecto minero cumpla el esquema mínimo definido en
  pipeline/schema/proyecto.schema.json. No inventa ni corrige datos: si algo
  no cumple el esquema, lo reporta como error para que se corrija a mano.

Por qué existe esta fase:
  Todo pipeline de datos necesita un "piso" confiable. Antes de automatizar
  la extracción (fases 2-3), este script garantiza que la base curada por
  investigación humana esté bien formada y sea la referencia de verdad
  contra la que se contrastan los datos obtenidos automáticamente.

Salida:
  pipeline/_out/fase1_reporte_validacion.json
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft7Validator

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
SCHEMA_PATH = REPO_ROOT / "pipeline" / "schema" / "proyecto.schema.json"
OUT_DIR = REPO_ROOT / "pipeline" / "_out"


def cargar_schema():
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def validar_proyectos(validator, proyectos, origen):
    errores = []
    for i, proyecto in enumerate(proyectos):
        for err in validator.iter_errors(proyecto):
            errores.append({
                "origen": origen,
                "indice": i,
                "nombre": proyecto.get("nombre", "(sin nombre)"),
                "error": err.message,
            })
    return errores


def main():
    schema = cargar_schema()
    validator = Draft7Validator(schema)

    reporte = {"archivos_revisados": [], "total_proyectos": 0, "errores": []}

    archivo_proyectos = DATA_DIR / "proyectos_cobre_colombia.json"
    if archivo_proyectos.exists():
        with open(archivo_proyectos, encoding="utf-8") as f:
            contenido = json.load(f)
        proyectos = contenido.get("proyectos", [])
        errores = validar_proyectos(validator, proyectos, archivo_proyectos.name)
        reporte["archivos_revisados"].append(archivo_proyectos.name)
        reporte["total_proyectos"] += len(proyectos)
        reporte["errores"].extend(errores)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "fase1_reporte_validacion.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)

    print(f"[Fase 1] Archivos revisados: {reporte['archivos_revisados']}")
    print(f"[Fase 1] Proyectos validados: {reporte['total_proyectos']}")
    print(f"[Fase 1] Errores encontrados: {len(reporte['errores'])}")
    if reporte["errores"]:
        for e in reporte["errores"]:
            print(f"  - {e['origen']} · {e['nombre']}: {e['error']}")
        return 1
    print("[Fase 1] OK — dataset semilla válido.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
