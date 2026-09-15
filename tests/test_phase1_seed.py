"""Tests de la Fase 1 (validación del esquema del dataset semilla)."""
from jsonschema import Draft7Validator

from pipeline.phase1_seed.validate_seed import cargar_schema, validar_proyectos


def test_el_esquema_real_del_repositorio_carga_sin_error():
    schema = cargar_schema()
    assert schema["required"] == ["nombre", "departamento", "operador", "estado"]


def test_proyecto_valido_no_produce_errores():
    validator = Draft7Validator(cargar_schema())
    proyecto_valido = {
        "nombre": "El Roble", "departamento": "Chocó",
        "operador": "Atico Mining Corporation", "estado": "En producción",
    }
    assert validar_proyectos(validator, [proyecto_valido], "test.json") == []


def test_proyecto_sin_campo_requerido_produce_error_con_su_nombre():
    validator = Draft7Validator(cargar_schema())
    proyecto_incompleto = {"nombre": "Proyecto Fantasma", "departamento": "Antioquia"}  # falta operador y estado
    errores = validar_proyectos(validator, [proyecto_incompleto], "test.json")
    assert len(errores) == 2  # falta 'operador' Y falta 'estado' -> 2 errores de jsonschema
    assert all(e["nombre"] == "Proyecto Fantasma" for e in errores)


def test_los_7_proyectos_reales_del_repositorio_pasan_el_esquema():
    """Test de integración liviano: no depende de red, solo lee el archivo
    ya versionado en el repo -- si alguien rompe data/proyectos_cobre_colombia.json
    al editarlo a mano, este test lo detecta sin tener que correr la Fase 1 completa."""
    import json
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[1]
    with open(repo_root / "data" / "proyectos_cobre_colombia.json", encoding="utf-8") as f:
        contenido = json.load(f)

    validator = Draft7Validator(cargar_schema())
    errores = validar_proyectos(validator, contenido["proyectos"], "proyectos_cobre_colombia.json")
    assert errores == []
    assert len(contenido["proyectos"]) >= 5
