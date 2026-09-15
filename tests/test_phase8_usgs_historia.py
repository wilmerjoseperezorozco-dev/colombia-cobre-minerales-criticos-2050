"""
Tests de la Fase 8 (USGS Data Series 140) contra un DataFrame pequeño
construido a mano que replica el formato real de la hoja 'Copper'
(encabezado 'Year' + filas de años + notas al pie que deben descartarse).
"""
import pandas as pd
import pytest

from pipeline.phase8_usgs_historia.fetch_usgs_ds140_copper import procesar_dataframe


@pytest.fixture
def df_copper():
    filas = [
        ["COPPER STATISTICS1"] + [None] * 12,
        ["U.S. GEOLOGICAL SURVEY"] + [None] * 12,
        ["[All values are in metric tons (t) copper content unless otherwise noted]"] + [None] * 12,
        ["Last modification: June 27, 2023"] + [None] * 12,
        ["Year", "Primary production", "Secondary production", "New scrap", "Refinery scrap",
         "Imports", "Exports", "Stocks", "Consumption", "Apparent consumption",
         "Unit value ($/t)", "Unit value (98$/t)", "World production"],
        [1900, 291000, None, None, None, 28000, 154000, 76000, 166000, 166000, 357, 7000, 495000],
        [1901, 302000, None, None, None, 32000, 88000, 128000, 118000, 194000, 355, 7000, 526000],
        [2020, 874000, 160000, 697000, 43200, 676000, 41200, 118000, 1770000, 1660000, 6320, 3980, 20600000],
        ["NA Not available."] + [None] * 12,
        ["1Compiled by K.E. Porter, D.L. Edelstein, M. Brininstool, and D.M. Flanagan."] + [None] * 12,
    ]
    return pd.DataFrame(filas)


def test_procesar_dataframe_encuentra_rango_de_anos(df_copper):
    resultado = procesar_dataframe(df_copper, url_xlsx="https://example.com/ds140-copper-2020.xlsx", extraido_utc="2026-09-14T00:00:00+00:00")
    assert resultado["rango_anos"] == [1900, 2020]
    assert resultado["num_anos"] == 3  # solo 1900, 1901, 2020 en este fixture reducido


def test_procesar_dataframe_descarta_filas_de_notas_al_pie(df_copper):
    resultado = procesar_dataframe(df_copper, url_xlsx="x")
    anos_extraidos = [r["ano"] for r in resultado["serie_completa"]]
    assert "NA Not available." not in anos_extraidos
    assert all(isinstance(a, int) for a in anos_extraidos)


def test_procesar_dataframe_extrae_fecha_de_ultima_modificacion(df_copper):
    resultado = procesar_dataframe(df_copper, url_xlsx="x")
    assert resultado["ultima_modificacion_reportada_por_usgs"] == "June 27, 2023"


def test_procesar_dataframe_valores_del_ultimo_registro_correctos(df_copper):
    resultado = procesar_dataframe(df_copper, url_xlsx="x")
    ultimo = resultado["ultimo_registro"]
    assert ultimo["ano"] == 2020
    assert ultimo["produccion_primaria_t"] == 874000
    assert ultimo["produccion_mundial_t"] == 20600000


def test_procesar_dataframe_falla_si_no_encuentra_encabezado_year():
    df_sin_encabezado = pd.DataFrame([["algo", "distinto"], ["1900", "291000"]])
    with pytest.raises(ValueError, match="Year"):
        procesar_dataframe(df_sin_encabezado, url_xlsx="x")
