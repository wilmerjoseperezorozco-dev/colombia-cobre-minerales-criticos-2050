"""
Tests de la Fase 2 (precio de cobre FRED) contra un CSV de muestra reducido
(14 filas, no las 415 reales) que preserva el formato exacto de columnas de
FRED y el último dato real observado (2026-07-01 = USD 13,542.82/t) para
poder afirmar un valor concreto conocido.
"""
from pathlib import Path

import pytest

from pipeline.phase2_live_fetch.fetch_copper_price_fred import parsear_csv_fred

FIXTURE = Path(__file__).parent / "fixtures" / "fred_pcoppusdm_muestra.csv"


@pytest.fixture
def csv_texto():
    return FIXTURE.read_text(encoding="utf-8")


def test_parsear_csv_fred_extrae_el_ultimo_dato_real(csv_texto):
    resultado = parsear_csv_fred(csv_texto, extraido_utc="2026-09-14T00:00:00+00:00")
    assert resultado["ultimo_dato"]["fecha"] == "2026-07-01"
    assert resultado["ultimo_dato"]["precio_usd_por_tonelada"] == 13542.82


def test_parsear_csv_fred_cuenta_observaciones_correctamente(csv_texto):
    resultado = parsear_csv_fred(csv_texto)
    assert resultado["num_observaciones"] == 14
    assert resultado["rango_fechas"] == ["2020-08-01", "2026-07-01"]


def test_parsear_csv_fred_ordena_por_fecha_aunque_el_csv_no_este_ordenado():
    csv_desordenado = "observation_date,PCOPPUSDM\n2026-01-01,9000\n2020-01-01,5000\n2023-01-01,8000\n"
    resultado = parsear_csv_fred(csv_desordenado)
    fechas = [r["fecha"] for r in resultado["serie_completa"]]
    assert fechas == sorted(fechas)


def test_parsear_csv_fred_falla_ruidosamente_si_cambian_las_columnas():
    """Guardrail: si FRED agrega o quita una columna, debe fallar con un
    error claro en vez de generar silenciosamente un JSON con datos mal
    alineados."""
    csv_con_columna_extra = "observation_date,PCOPPUSDM,columna_nueva\n2026-01-01,9000,algo\n"
    with pytest.raises(ValueError, match="2 columnas"):
        parsear_csv_fred(csv_con_columna_extra)


def test_parsear_csv_fred_falla_si_no_hay_filas_numericas_validas():
    csv_vacio_de_datos = "observation_date,PCOPPUSDM\n.,.\n"
    with pytest.raises(ValueError, match="ninguna fila numérica válida"):
        parsear_csv_fred(csv_vacio_de_datos)


def test_estadisticas_5_anos_usan_ventana_correcta(csv_texto):
    resultado = parsear_csv_fred(csv_texto)
    # La ventana de 5 años desde 2026-07-01 excluye las filas de 2020-08 y
    # 2020-09 (2021-08-01 en adelante sí entra).
    assert resultado["estadisticas_5_anos"]["maximo"] == 13542.82
