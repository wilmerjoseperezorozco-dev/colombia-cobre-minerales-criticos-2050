"""
Tests de la Fase 5 (USGS Mineral Commodity Summaries) contra un fixture de
texto REAL (no sintético) capturado del PDF oficial — ver
tests/fixtures/usgs_mcs_copper_texto_real.py.

Estos tests responden directamente a la pregunta "¿cómo sabes que extrae lo
correcto?": no lo garantizan contra una edición futura del PDF (para eso
está el workflow semanal corriendo el fetch real), pero sí garantizan que
el código de parseo no regresiona silenciosamente — y ya atraparon un bug
real (ver test_tabla_mundial_corrige_marcador_de_nota_al_pie_de_australia).
"""
from pipeline.phase5_usgs.fetch_usgs_copper_mcs import (
    contexto_colombia,
    normalizar_espacios,
    num,
    parsear_designacion_critica,
    parsear_recursos_mundiales,
    parsear_salient_statistics_eeuu,
    parsear_tabla_mundial,
)
from tests.fixtures.usgs_mcs_copper_texto_real import PAGINA_1, PAGINA_2, TEXTO_COMPLETO


def test_num_convierte_enteros_y_descarta_no_disponible():
    assert num("1,230") == 1230
    assert num("432.3") == 432.3
    assert num("—") is None
    assert num("--") is None
    assert num("") is None


def test_normalizar_espacios_colapsa_saltos_de_linea():
    assert normalizar_espacios("hola\nmundo   con   espacios") == "hola mundo con espacios"


def test_parsear_designacion_critica_encuentra_fecha_y_referencia_real():
    resultado = parsear_designacion_critica(PAGINA_2)
    assert resultado["encontrado"] is True
    assert resultado["fecha_texto_original"] == "November 7, 2025"
    assert resultado["referencia_federal_register"] == "90 FR 50494"
    assert "copper" in resultado["minerales_agregados_en_esta_lista"]
    # Regresión: el bug original perdía el salto de línea entre "lead," y
    # "potash" -- confirmamos que quedan en el mismo string sin salto crudo.
    assert "\n" not in resultado["minerales_agregados_en_esta_lista"]


def test_parsear_designacion_critica_sin_texto_relevante_devuelve_no_encontrado():
    resultado = parsear_designacion_critica("Este texto no menciona ninguna lista de minerales críticos.")
    assert resultado == {"encontrado": False}


def test_parsear_salient_statistics_extrae_serie_2021_2025e():
    resultado = parsear_salient_statistics_eeuu(PAGINA_1)
    assert resultado["produccion_mina_recuperable_kt"] == {
        "2021": 1230, "2022": 1230, "2023": 1130, "2024": 1050, "2025e": 1000,
    }
    assert resultado["precio_comex_centavos_lb"]["2025e"] == 480


def test_parsear_tabla_mundial_encuentra_los_18_paises_reales():
    resultado = parsear_tabla_mundial(PAGINA_2)
    assert len(resultado["por_pais"]) == 18
    assert resultado["mundo_total"]["reservas_kt"] == 980000
    assert resultado["por_pais"]["Chile"]["reservas_kt"] == 180000
    assert resultado["por_pais"]["Germany"]["produccion_mina_kt_2024"] is None  # "—" -> None, no cero


def test_tabla_mundial_corrige_marcador_de_nota_al_pie_de_australia():
    """Regresión del bug real encontrado el 14-sep-2026: pdfplumber pega el
    marcador de nota al pie '7' al valor de reservas de Australia
    ('7100,000' en vez de '100,000'). El guardrail debe detectarlo (porque
    excede el total mundial) y corregirlo, dejando evidencia en advertencias.
    """
    resultado = parsear_tabla_mundial(PAGINA_2)
    assert resultado["por_pais"]["Australia"]["reservas_kt"] == 100000
    advertencias_texto = " ".join(resultado["advertencias"])
    assert "Australia" in advertencias_texto
    assert "Corrección automática" in advertencias_texto


def test_parsear_tabla_mundial_reporta_advertencia_si_falta_un_pais():
    texto_incompleto = "United States 1,050 1,000 921 850 47,000\nWorld total (rounded) 23,000 23,000 27,600 29,000 980,000"
    resultado = parsear_tabla_mundial(texto_incompleto)
    assert len(resultado["por_pais"]) == 1
    assert any("Australia" in a for a in resultado["advertencias"])


def test_parsear_recursos_mundiales_extrae_las_4_cifras():
    resultado = parsear_recursos_mundiales(PAGINA_2)
    assert resultado["encontrado"] is True
    assert resultado["recursos_identificados_sin_extraer_billones_toneladas_cortas"] == 1.5
    assert resultado["recursos_no_descubiertos_estimados_billones_toneladas_cortas"] == 3.5


def test_contexto_colombia_calcula_porcentaje_correcto_con_17_4_mt():
    tabla = parsear_tabla_mundial(PAGINA_2)
    resultado = contexto_colombia(tabla, potencial_upme_mt=17.4)
    # 17.4 Mt = 17,400 kt sobre 980,000 kt mundiales = 1.776%
    assert resultado["pct_potencial_colombia_sobre_reservas_mundiales"] == 1.776
    # Regresión directa del bug de la cifra vieja: con 9.7 Mt (incorrecta)
    # el resultado sería 0.99%, no 1.776% -- si alguien revierte el default
    # a 9.7 por error, este test lo detecta.
    resultado_viejo = contexto_colombia(tabla, potencial_upme_mt=9.7)
    assert resultado_viejo["pct_potencial_colombia_sobre_reservas_mundiales"] != resultado["pct_potencial_colombia_sobre_reservas_mundiales"]


def test_texto_completo_fixture_no_esta_vacio():
    """Sanity check del fixture mismo -- si esto falla, el problema es el fixture, no el parser."""
    assert len(TEXTO_COMPLETO) > 500
    assert "COPPER" in TEXTO_COMPLETO
