"""
Tests de la Fase 9 (auditoría de catálogo de tablas de UPME).

Cubre específicamente la regresión del falso positivo real que se encontró
al construir esta fase: el clasificador inicial confundía "recurso
hídrico" (categoría ambiental) con un recurso mineral, porque buscaba la
palabra genérica "recurso". Ver docs/09-metodologia-pipeline.md, sección
2.5, para el relato completo del bug y la corrección.
"""
from pipeline.phase9_upme_auditoria.audit_upme_docs_adicionales import clasificar_tabla


def test_clasifica_tabla_de_recursos_minerales_correctamente():
    # Nota: "Recursos proyecto el Roble" y "Recursos Minerales" caen a
    # propósito en 'ya_cubierta_por_fase_7' porque son los títulos EXACTOS
    # de tablas que la Fase 7 ya extrae (ver PALABRAS_YA_CUBIERTAS) -- eso
    # se prueba aparte en test_tabla_ya_cubierta_por_fase_7_se_marca_explicitamente.
    # Una tabla de recursos que NO coincide con esos títulos exactos sí debe
    # caer en 'recursos_reservas':
    assert clasificar_tabla("Tenor y ley de Cu del yacimiento") == "recursos_reservas"
    assert clasificar_tabla("Potencial de mineral de cobre en Colombia por región") == "recursos_reservas"


def test_no_confunde_recurso_hidrico_con_recurso_mineral():
    """Regresión directa del bug real: 'recurso hídrico' debe ir a
    'ambiental', nunca a 'recursos_reservas', aunque contenga la palabra
    'recurso'."""
    resultado = clasificar_tabla("Identificación del recurso hídrico del área intervenida por el Proyecto El Roble")
    assert resultado == "ambiental"
    assert resultado != "recursos_reservas"


def test_clasifica_tabla_economica():
    assert clasificar_tabla("Producto Interno Bruto PIB por actividades económicas Chocó") == "economico_financiero"


def test_clasifica_tabla_demografica():
    assert clasificar_tabla("Población por área geográfica - territorio de análisis proyecto El Roble") == "demografico_social"


def test_tabla_ya_cubierta_por_fase_7_se_marca_explicitamente():
    assert clasificar_tabla("Resumen comparativo impactos económicos") == "ya_cubierta_por_fase_7"


def test_tabla_sin_palabras_clave_queda_sin_clasificar():
    assert clasificar_tabla("Un título completamente genérico sin señales") == "otro_sin_clasificar"
