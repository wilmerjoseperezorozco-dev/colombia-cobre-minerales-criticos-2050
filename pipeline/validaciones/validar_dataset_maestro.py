"""
GUARDRAIL — validación de consistencia sobre el dataset maestro consolidado.

Por qué existe este archivo (respuesta directa a una revisión externa):
  Hasta el 14-sep-2026, ninguna fase del pipeline validaba automáticamente
  que los números extraídos fueran *lógicamente consistentes entre sí* —
  solo se validaba que el JSON tuviera el esquema esperado (Fase 1) y que
  cada parser individual no lanzara una excepción. Esto es un hueco real:
  la corrección de "9.7 Mt -> 17.4 Mt" (Fase 7) y el bug de reservas de
  Australia ("7.100.000 -> 100.000", Fase 5) se encontraron los DOS
  leyendo el resultado a ojo, no por un guardrail automatizado.

  Este módulo no pretende cerrar ese hueco por completo (haría falta un
  modelo de validación cruzada mucho más elaborado), pero sí implementa
  las comprobaciones lógicas más baratas y de mayor valor: invariantes que
  NUNCA deberían violarse si los datos son correctos, sin importar qué
  edición de qué fuente se haya usado.

Qué SÍ detecta:
  - Un país con más reservas que el total mundial (el bug real de Australia).
  - El potencial de Colombia superando las reservas mundiales totales.
  - Un precio de cobre fuera de un rango físicamente plausible.
  - Un bloque del dataset maestro sin la etiqueta de procedencia ("origen").

Qué NO detecta (limitación explícita, no oculta):
  - Que una cifra sea correcta en términos absolutos — solo que sea
    *consistente* con las demás. Un error que afecte a dos fuentes por
    igual (ej. ambas mal convertidas de toneladas cortas a métricas)
    pasaría estas validaciones sin ser detectado.
  - Cambios de formato en una fuente que produzcan un valor "razonable"
    pero incorrecto (ej. si USGS reordenara las columnas de la tabla
    mundial de forma que un país tomara el valor de otro país vecino con
    magnitud similar).

Uso:
  python pipeline/validaciones/validar_dataset_maestro.py
  (se ejecuta automáticamente al final de pipeline/run_pipeline.py)
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[2]
DATASET_MAESTRO = REPO_ROOT / "data" / "consolidado" / "dataset_maestro.json"

PRECIO_COBRE_USD_TONELADA_MIN = 1000
PRECIO_COBRE_USD_TONELADA_MAX = 50000


def cargar_dataset() -> dict:
    with open(DATASET_MAESTRO, encoding="utf-8") as f:
        return json.load(f)


def validar_procedencia_de_cada_bloque(dataset: dict) -> list[str]:
    errores = []
    for nombre, bloque in dataset.get("bloques", {}).items():
        if not bloque.get("origen"):
            errores.append(f"El bloque '{nombre}' no tiene etiqueta de procedencia ('origen').")
    return errores


def validar_reservas_por_pais_no_exceden_el_total(dataset: dict) -> list[str]:
    errores = []
    usgs = dataset["bloques"].get("usgs_mineral_commodity_summaries_copper", {}).get("datos", {})
    tabla = usgs.get("produccion_y_reservas_mundiales", {})
    total = tabla.get("mundo_total") or {}
    for pais, valores in (tabla.get("por_pais") or {}).items():
        for campo, valor in valores.items():
            tope = total.get(campo)
            if valor is not None and tope is not None and valor > tope:
                errores.append(
                    f"USGS: '{pais}'.{campo} = {valor} excede el total mundial declarado ({tope}) — "
                    f"posible marcador de nota al pie sin corregir o error de fuente."
                )
    return errores


def validar_potencial_colombia_no_excede_reservas_mundiales(dataset: dict) -> list[str]:
    errores = []
    potencial = dataset["bloques"].get("potencial_colombia_y_retos", {}).get("datos", {})
    potencial_mt = (potencial.get("potencial_geologico") or {}).get("potencial_colombia_propio_total_mt_cu")

    usgs = dataset["bloques"].get("usgs_mineral_commodity_summaries_copper", {}).get("datos", {})
    reservas_mundiales_kt = ((usgs.get("produccion_y_reservas_mundiales") or {}).get("mundo_total") or {}).get("reservas_kt")

    if potencial_mt is not None and reservas_mundiales_kt is not None:
        if (potencial_mt * 1000) > reservas_mundiales_kt:
            errores.append(
                f"El potencial de Colombia ({potencial_mt} Mt) excede las reservas mundiales "
                f"totales reportadas por USGS ({reservas_mundiales_kt} kt) — imposible lógicamente."
            )
    return errores


def validar_precio_cobre_en_rango_plausible(dataset: dict) -> list[str]:
    errores = []
    precio = dataset["bloques"].get("precio_cobre_serie_historica", {}).get("datos", {})
    ultimo = (precio or {}).get("ultimo_dato", {}).get("precio_usd_por_tonelada")
    if ultimo is not None and not (PRECIO_COBRE_USD_TONELADA_MIN <= ultimo <= PRECIO_COBRE_USD_TONELADA_MAX):
        errores.append(
            f"El último precio de cobre ({ultimo} USD/t) está fuera del rango plausible "
            f"[{PRECIO_COBRE_USD_TONELADA_MIN}, {PRECIO_COBRE_USD_TONELADA_MAX}] — revisar la fuente."
        )
    return errores


def validar_demanda_iea_vs_oferta_usgs_orden_de_magnitud(dataset: dict) -> list[str]:
    """No es un error si difieren -- distintas metodologías (ver docs/10,
    sección 3.4). Pero si difirieran en un orden de magnitud completo
    (ej. una en kt y otra sin convertir de toneladas), sí sería señal de
    un bug de unidades -- eso es lo único que esta comprobación vigila."""
    advertencias = []
    iea = dataset["bloques"].get("iea_critical_minerals_demanda_oferta_cobre", {}).get("datos", {})
    demanda_2025 = ((iea.get("demanda_cobre") or {}).get("2025_linea_base") or {}).get("total_demanda")

    usgs = dataset["bloques"].get("usgs_mineral_commodity_summaries_copper", {}).get("datos", {})
    refineria_2025e = ((usgs.get("estadisticas_eeuu_serie_2021_2025e") or {}).get("refinacion_primaria_kt") or {}).get("2025e")

    if demanda_2025 is not None and refineria_2025e is not None and refineria_2025e > 0:
        razon = demanda_2025 / refineria_2025e
        # La demanda IEA es global; la refinación aquí es solo de EE.UU. -- se
        # espera que la razón sea grande (EE.UU. es una fracción del mundo),
        # pero no descabelladamente grande (>1000x) ni invertida (<1x).
        if not (1 <= razon <= 1000):
            advertencias.append(
                f"Razón demanda IEA global 2025 ({demanda_2025} kt) / refinación primaria EE.UU. 2025e "
                f"({refineria_2025e} kt) = {razon:.1f}x, fuera del rango esperado [1x, 1000x] -- revisar unidades."
            )
    return advertencias


VALIDACIONES = [
    ("Procedencia de cada bloque", validar_procedencia_de_cada_bloque, True),
    ("Reservas por país <= total mundial (USGS)", validar_reservas_por_pais_no_exceden_el_total, True),
    ("Potencial de Colombia <= reservas mundiales", validar_potencial_colombia_no_excede_reservas_mundiales, True),
    ("Precio del cobre en rango plausible", validar_precio_cobre_en_rango_plausible, True),
    ("Orden de magnitud demanda IEA vs. refinación USGS", validar_demanda_iea_vs_oferta_usgs_orden_de_magnitud, False),
]


def main() -> int:
    if not DATASET_MAESTRO.exists():
        print(f"[Guardrail] {DATASET_MAESTRO} no existe todavía — correr primero la Fase 4.")
        return 1

    dataset = cargar_dataset()
    hubo_error_bloqueante = False

    print("=" * 70)
    print("Guardrail de consistencia — dataset_maestro.json")
    print("=" * 70)

    for nombre, funcion, es_bloqueante in VALIDACIONES:
        problemas = funcion(dataset)
        etiqueta = "ERROR" if es_bloqueante else "ADVERTENCIA"
        if problemas:
            if es_bloqueante:
                hubo_error_bloqueante = True
            print(f"\n[{etiqueta}] {nombre}:")
            for p in problemas:
                print(f"    - {p}")
        else:
            print(f"[OK] {nombre}")

    print("\n" + "=" * 70)
    if hubo_error_bloqueante:
        print("Guardrail FALLÓ — hay inconsistencias lógicas que requieren revisión antes de publicar.")
        return 1
    print("Guardrail OK — sin inconsistencias lógicas detectadas (ver limitaciones en el docstring).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
