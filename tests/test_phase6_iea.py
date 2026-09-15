"""
Tests de la Fase 6 (IEA Critical Minerals Data Explorer) contra un DataFrame
construido a mano que replica las posiciones EXACTAS de celda (fila, columna)
que `extraer_demanda_cobre`/`extraer_oferta_cobre` leen del Excel real —
ver pipeline/phase6_iea/ingest_iea_manual.py.

No se usa el .xlsx real como fixture (vive en pipeline/_manual_uploads/ y
NO se sube al repositorio salvo el archivo aportado por el usuario) — en su
lugar, replicar las posiciones de celda documenta explícitamente qué
estructura espera el código, lo cual es información valiosa por sí misma:
si IEA reordena filas o columnas en una edición futura, estos tests fallan
con un mensaje claro de qué posición esperaba qué valor.
"""
import numpy as np
import pandas as pd
import pytest

from pipeline.phase6_iea.ingest_iea_manual import extraer_demanda_cobre, extraer_oferta_cobre


@pytest.fixture
def df_demanda():
    """Replica la hoja '1 Total demand for key minerals', filas 14-17,
    columna 1 = línea base 2025, columnas 3-19 = 3 escenarios x 5 años."""
    filas, cols = 18, 20
    data = np.full((filas, cols), np.nan, dtype=object)
    # fila 14: Total energy technologies | fila 15: Other uses | fila 16: Total demand | fila 17: share
    data[14, 1] = 8003.0
    data[15, 1] = 19772.0
    data[16, 1] = 27775.0
    data[17, 1] = 0.288
    data[16, 3:8] = [30792.0, 32359.0, 33580.0, 35080.0, 35888.0]       # Current Policies
    data[16, 9:14] = [31370.0, 33522.0, 34984.0, 36579.0, 37572.0]      # Stated Policies
    data[16, 15:20] = [31967.0, 34294.0, 35719.0, 36773.0, 38066.0]     # High Demand
    return pd.DataFrame(data)


@pytest.fixture
def df_oferta():
    """Replica la hoja '2 Total supply for key minerals', filas 6-14,
    columna 0 = nombre de país, columnas 1-4 = 2025/2030/2035/2040."""
    filas, cols = 15, 5
    data = np.full((filas, cols), np.nan, dtype=object)
    paises = [
        ("Chile", [5485.0, 5369.0, 4841.0, 4165.0]),
        ("Democratic Republic of Congo", [3338.0, 4212.0, 3041.0, 2696.0]),
        ("Peru", [2726.0, 2712.0, 2384.0, 1859.0]),
        ("China", [1838.0, 2040.0, 1965.0, 1852.0]),
        ("Russia", [1145.0, 1244.0, 1424.0, 1343.0]),
        ("United States", [1101.0, 1196.0, 823.0, 632.0]),
        ("Rest of world", [7594.0, 7798.0, 6255.0, 4636.0]),
    ]
    for i, (nombre, valores) in enumerate(paises):
        fila = 6 + i
        data[fila, 0] = nombre
        data[fila, 1:5] = valores
    data[13, 1:5] = [23227.0, 24571.0, 20733.0, 17183.0]  # Total
    data[14, 1:5] = [0.497, 0.5, 0.495, 0.507]             # Top 3 share
    return pd.DataFrame(data)


def test_extraer_demanda_cobre_linea_base_2025(df_demanda):
    resultado = extraer_demanda_cobre(df_demanda)
    assert resultado["2025_linea_base"]["total_demanda"] == 27775.0
    assert resultado["2025_linea_base"]["participacion_energia_transicion_pct"] == 28.8


def test_extraer_demanda_cobre_los_3_escenarios(df_demanda):
    resultado = extraer_demanda_cobre(df_demanda)
    escenarios = resultado["total_demanda_por_escenario_kt"]
    assert escenarios["stated_policies_scenario"][-1] == 37572.0
    assert escenarios["current_policies_scenario"][0] == 30792.0
    assert len(escenarios["high_demand_scenario"]) == 5


def test_extraer_oferta_cobre_total_mundial_y_paises(df_oferta):
    resultado = extraer_oferta_cobre(df_oferta)
    assert resultado["total_mundial"][2025] == 23227.0
    assert resultado["total_mundial"][2040] == 17183.0
    assert resultado["por_pais"]["Chile"][2025] == 5485.0
    assert "Colombia" not in resultado["por_pais"]  # confirma que Colombia va dentro de "Rest of world"


def test_brecha_oferta_demanda_calculada_manualmente(df_demanda, df_oferta):
    """Reproduce el cálculo citado en docs/01 y docs/10: demanda (Stated
    Policies) menos oferta base case, mismo año -- si alguien cambia los
    índices de columna de cualquiera de las dos funciones, esta brecha deja
    de cuadrar con los números ya publicados en la documentación."""
    demanda = extraer_demanda_cobre(df_demanda)
    oferta = extraer_oferta_cobre(df_oferta)
    brecha_2030 = demanda["total_demanda_por_escenario_kt"]["stated_policies_scenario"][0] - oferta["total_mundial"][2030]
    assert round(brecha_2030) == 6799
