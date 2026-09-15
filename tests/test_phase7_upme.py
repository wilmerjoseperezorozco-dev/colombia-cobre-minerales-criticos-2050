"""
Tests de la Fase 7 (Informe Cobre de UPME) contra texto REAL extraído del
PDF oficial — ver tests/fixtures/upme_informe_cobre_texto_real.py.

Estos tests son, en cierto sentido, los más importantes de todo el
repositorio: la Fase 7 fue la que produjo la corrección metodológica de
"9.7 Mt -> 17.4 Mt" documentada en docs/10, sección 3.5. Antes de esta
tarea, esa corrección se validó leyendo el PDF a ojo, sin ningún guardrail
automatizado -- exactamente el hueco que este archivo empieza a cerrar.
"""
from pipeline.phase7_upme_sgc.fetch_upme_informe_cobre import (
    normalizar,
    num,
    parsear_el_roble,
    parsear_potencial_nacional,
)
from tests.fixtures.upme_informe_cobre_texto_real import (
    TABLA_1_POTENCIAL_NACIONAL,
    TABLA_2_EL_ROBLE,
    TEXTO_TEXTO_LIBRE_POTENCIAL_COLOMBIA,
)


def test_num_convierte_con_comas_de_miles():
    assert num("1,039,200") == 1039200
    assert num("4.34") == 4.34


def test_normalizar_colapsa_espacios():
    assert normalizar("a   b\nc") == "a b c"


class TestParsearPotencialNacional:
    """Estos tests son la regresión directa de la corrección 9.7 -> 17.4 Mt."""

    def setup_method(self):
        self.resultado = parsear_potencial_nacional(
            [TABLA_1_POTENCIAL_NACIONAL, TEXTO_TEXTO_LIBRE_POTENCIAL_COLOMBIA]
        )

    def test_encuentra_las_5_filas_usgs(self):
        assert len(self.resultado["detalle_por_region_usgs"]) == 5

    def test_el_promedio_compartido_es_37_3_no_el_total_de_colombia(self):
        assert self.resultado["promedio_regiones_compartidas_mt"] == 37.3

    def test_el_potencial_propio_de_colombia_es_17_4_no_9_7(self):
        """Esta es LA aserción que habría detectado el error original si
        hubiera existido este test antes de la corrección."""
        assert self.resultado["potencial_colombia_propio_mt"] == [7.7, 9.7]
        assert self.resultado["potencial_colombia_propio_total_mt"] == 17.4

    def test_plate_25_y_26_son_las_regiones_propias_de_colombia(self):
        propias = {f["plate"]: f["recursos_estimados_in_situ_mt"] for f in self.resultado["detalle_por_region_usgs"]}
        assert propias[25] == 7.7
        assert propias[26] == 9.7
        # Plate 22, la primera de las 3 compartidas, NO debe confundirse con una propia
        assert propias[22] == 39.0


def test_parsear_el_roble_extrae_las_4_categorias_de_recursos():
    resultado = parsear_el_roble([TABLA_2_EL_ROBLE])
    recursos = resultado["recursos"]
    assert recursos["recursos_medidos"]["mena_t"] == 1039200
    assert recursos["recursos_medidos"]["cu_pct"] == 4.34
    assert recursos["medidos_mas_indicados"]["cu_lb_contenido"] == 84343400
    assert recursos["recursos_inferidos"]["au_g_t"] == 3.41


def test_parsear_el_roble_no_inventa_categorias_si_el_texto_esta_incompleto():
    """Si el bloque de texto no tiene las 4 filas (ej. un PDF futuro con
    formato distinto), la función debe devolver solo lo que sí encontró,
    no fallar en silencio con datos incompletos disfrazados de completos."""
    resultado = parsear_el_roble(["Tabla 2. Recursos proyecto el Roble\nRecursos 1,000 5.0 2.0 100,000 1,000 Medidos\n2.2.2."])
    assert "recursos_medidos" in resultado["recursos"]
    assert "recursos_indicados" not in resultado["recursos"]
