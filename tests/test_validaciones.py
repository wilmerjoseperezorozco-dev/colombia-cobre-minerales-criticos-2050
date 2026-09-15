"""
Tests del guardrail de consistencia (pipeline/validaciones/validar_dataset_maestro.py).

Estos tests validan al validador: construyen un dataset_maestro sintético
con un problema conocido inyectado a propósito, y confirman que la
función correspondiente lo detecta -- incluyendo una reproducción exacta
del bug real de Australia (Fase 5) que motivó este guardrail.
"""
from pipeline.validaciones.validar_dataset_maestro import (
    validar_demanda_iea_vs_oferta_usgs_orden_de_magnitud,
    validar_potencial_colombia_no_excede_reservas_mundiales,
    validar_precio_cobre_en_rango_plausible,
    validar_procedencia_de_cada_bloque,
    validar_reservas_por_pais_no_exceden_el_total,
)


def _dataset_base() -> dict:
    return {
        "bloques": {
            "usgs_mineral_commodity_summaries_copper": {
                "origen": "api_publica_en_vivo",
                "datos": {
                    "produccion_y_reservas_mundiales": {
                        "por_pais": {"Chile": {"reservas_kt": 180000}},
                        "mundo_total": {"reservas_kt": 980000},
                    },
                    "estadisticas_eeuu_serie_2021_2025e": {
                        "refinacion_primaria_kt": {"2025e": 790},
                    },
                },
            },
            "potencial_colombia_y_retos": {
                "origen": "curado_investigacion_humana",
                "datos": {"potencial_geologico": {"potencial_colombia_propio_total_mt_cu": 17.4}},
            },
            "precio_cobre_serie_historica": {
                "origen": "api_publica_en_vivo",
                "datos": {"ultimo_dato": {"precio_usd_por_tonelada": 13542.82}},
            },
            "iea_critical_minerals_demanda_oferta_cobre": {
                "origen": "aportado_manualmente_por_usuario",
                "datos": {"demanda_cobre": {"2025_linea_base": {"total_demanda": 27775}}},
            },
        }
    }


def test_dataset_valido_no_produce_errores():
    dataset = _dataset_base()
    assert validar_procedencia_de_cada_bloque(dataset) == []
    assert validar_reservas_por_pais_no_exceden_el_total(dataset) == []
    assert validar_potencial_colombia_no_excede_reservas_mundiales(dataset) == []
    assert validar_precio_cobre_en_rango_plausible(dataset) == []


def test_detecta_bloque_sin_procedencia():
    dataset = _dataset_base()
    dataset["bloques"]["bloque_nuevo_sin_etiquetar"] = {"datos": {}}  # sin "origen"
    errores = validar_procedencia_de_cada_bloque(dataset)
    assert len(errores) == 1
    assert "bloque_nuevo_sin_etiquetar" in errores[0]


def test_reproduce_el_bug_real_de_australia():
    """Si este guardrail hubiera existido antes del 14-sep-2026, habría
    atrapado el bug real de Australia (reservas 7,100,000 en vez de
    100,000) apenas se generó el dataset, no varias corridas después."""
    dataset = _dataset_base()
    dataset["bloques"]["usgs_mineral_commodity_summaries_copper"]["datos"][
        "produccion_y_reservas_mundiales"
    ]["por_pais"]["Australia"] = {"reservas_kt": 7100000}
    errores = validar_reservas_por_pais_no_exceden_el_total(dataset)
    assert len(errores) == 1
    assert "Australia" in errores[0]
    assert "7100000" in errores[0]


def test_detecta_potencial_de_colombia_imposible():
    dataset = _dataset_base()
    dataset["bloques"]["potencial_colombia_y_retos"]["datos"]["potencial_geologico"][
        "potencial_colombia_propio_total_mt_cu"
    ] = 5000  # 5,000 Mt -- mayor que las reservas mundiales totales, imposible
    errores = validar_potencial_colombia_no_excede_reservas_mundiales(dataset)
    assert len(errores) == 1


def test_detecta_precio_de_cobre_fuera_de_rango():
    dataset = _dataset_base()
    dataset["bloques"]["precio_cobre_serie_historica"]["datos"]["ultimo_dato"]["precio_usd_por_tonelada"] = 500000
    errores = validar_precio_cobre_en_rango_plausible(dataset)
    assert len(errores) == 1


def test_advertencia_de_orden_de_magnitud_no_dispara_con_datos_normales():
    dataset = _dataset_base()
    assert validar_demanda_iea_vs_oferta_usgs_orden_de_magnitud(dataset) == []


def test_advertencia_de_orden_de_magnitud_si_hay_error_de_unidades():
    dataset = _dataset_base()
    # Simula un error de unidades: refinación en toneladas en vez de kt (factor 1000 de más)
    dataset["bloques"]["usgs_mineral_commodity_summaries_copper"]["datos"][
        "estadisticas_eeuu_serie_2021_2025e"
    ]["refinacion_primaria_kt"]["2025e"] = 790000
    advertencias = validar_demanda_iea_vs_oferta_usgs_orden_de_magnitud(dataset)
    assert len(advertencias) == 1
