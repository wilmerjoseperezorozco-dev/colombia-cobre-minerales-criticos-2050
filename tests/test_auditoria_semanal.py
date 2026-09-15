"""
Tests de `pipeline/auditoria_semanal/comparar_dataset_maestro.py` -- la
lógica pura de comparación/detección de anomalías, con fixtures sintéticos
pequeños (no los dataset_maestro.json reales de 150+ campos, que harían el
test frágil ante cualquier cambio de contenido no relacionado)."""
from pipeline.auditoria_semanal.comparar_dataset_maestro import (
    UMBRAL_ALERTA_PCT,
    comparar_valores_clave,
)


def _dataset_base(precio_actual=13500, cagr=7.5, potencial_mt=17.4, demanda_kt=27775, pct_reservas=1.78):
    return {
        "bloques": {
            "precio_cobre_serie_historica": {
                "datos": {"serie_completa": [{"fecha": "2026-08-01", "precio_usd_por_tonelada": precio_actual}]},
                "metricas_calculadas": {"cagr_5_anos_pct": cagr},
            },
            "potencial_colombia_y_retos": {
                "datos": {"potencial_geologico": {"potencial_colombia_propio_total_mt_cu": potencial_mt}},
            },
            "demanda_global_cobre": {
                "datos": {"demanda_total_cobre_iea_2026_kt": {"2025_linea_base": demanda_kt}},
            },
            "usgs_mineral_commodity_summaries_copper": {
                "datos": {"contexto_colombia_vs_usgs": {"pct_potencial_colombia_sobre_reservas_mundiales": pct_reservas}},
            },
        }
    }


def test_sin_cambios_no_genera_alertas():
    previo = _dataset_base()
    actual = _dataset_base()
    resultado = comparar_valores_clave(actual, previo)
    assert resultado["alertas"] == []
    variaciones = {c["campo"]: c["variacion_pct"] for c in resultado["campos"]}
    assert variaciones["precio_cobre_ultimo_valor_usd_por_tonelada"] == 0.0


def test_variacion_pequena_no_dispara_alerta():
    """Un movimiento normal de mercado (ej. +3% en el precio semana a
    semana) no debe marcarse como anomalía -- solo cambios grandes."""
    previo = _dataset_base(precio_actual=13500)
    actual = _dataset_base(precio_actual=13905)  # +3%
    resultado = comparar_valores_clave(actual, previo)
    assert resultado["alertas"] == []


def test_caida_de_precio_mayor_a_50_por_ciento_dispara_alerta():
    """El caso concreto que pidió la revisión: una caída de precio >50% de
    una semana a otra probablemente sea un error de la fuente, no un
    movimiento real -- debe quedar marcada."""
    previo = _dataset_base(precio_actual=13500)
    actual = _dataset_base(precio_actual=4000)  # -70.4%
    resultado = comparar_valores_clave(actual, previo)
    assert len(resultado["alertas"]) == 1
    assert "precio_cobre_ultimo_valor_usd_por_tonelada" in resultado["alertas"][0]
    campo = next(c for c in resultado["campos"] if c["campo"] == "precio_cobre_ultimo_valor_usd_por_tonelada")
    assert campo["variacion_pct"] < -UMBRAL_ALERTA_PCT


def test_campo_ausente_en_el_snapshot_previo_no_revienta():
    """Un dataset viejo (de antes de que existiera un campo) es un caso
    normal -- no debe lanzar KeyError, solo dejar variacion_pct en None."""
    previo = {"bloques": {}}  # snapshot "vacío", simula un dataset muy antiguo
    actual = _dataset_base()
    resultado = comparar_valores_clave(actual, previo)
    assert resultado["alertas"] == []  # None no es comparable numéricamente, no dispara alerta
    variaciones = {c["campo"]: c["variacion_pct"] for c in resultado["campos"]}
    assert all(v is None for v in variaciones.values())


def test_multiples_campos_anomalos_generan_multiples_alertas():
    previo = _dataset_base(precio_actual=13500, potencial_mt=17.4)
    actual = _dataset_base(precio_actual=13500, potencial_mt=2.0)  # caída fuerte y no realista
    resultado = comparar_valores_clave(actual, previo)
    campos_con_alerta = {a.split(":")[0] for a in resultado["alertas"]}
    assert "potencial_colombia_total_mt_cu" in campos_con_alerta
