"""
FASE 8 — Serie histórica de cobre en EE. UU. desde 1900 (USGS Data Series 140).

Fuente:
  USGS Data Series 140, "Historical Statistics for Mineral and Material
  Commodities in the United States" — ficha de Copper. La página de
  aterrizaje es HTML (Drupal); el archivo real es un .xlsx alojado en un
  bucket S3 de USGS con nombre versionado (ej. "ds140-copper-2020.xlsx").
  Este script NO hardcodea ese nombre: descarga la página HTML, extrae el
  enlace `.xlsx` vigente con una expresión regular, y descarga ese archivo
  — así sigue funcionando si USGS publica una actualización con otro año
  en el nombre del archivo.

Qué complementa en el pipeline:
  La Fase 2 (FRED) cubre precio mensual de cobre 1992-2026. Esta fase
  aporta el siglo previo (1900-2020) de datos de EE. UU.: producción
  primaria y secundaria, importaciones/exportaciones, consumo, valor
  unitario nominal y ajustado por inflación (dólares de 1998), y
  producción mundial — permitiendo poner el régimen de precios actual
  (CAGR 7.46% a 5 años, ver Fase 2) en perspectiva de más de un siglo.

Salida:
  data/live/usgs_ds140_copper_historia.json
  pipeline/_out/ds140-copper-*.xlsx (copia cruda, auditoría)
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "data" / "live"
PDF_CACHE_DIR = REPO_ROOT / "pipeline" / "_out"

URL_LANDING = "https://www.usgs.gov/media/files/copper-historical-statistics-data-series-140"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

COLUMNAS = [
    "produccion_primaria_t", "produccion_secundaria_t", "chatarra_nueva_t",
    "chatarra_refineria_t", "importaciones_t", "exportaciones_t", "existencias_t",
    "consumo_t", "consumo_aparente_t", "valor_unitario_usd_por_t_nominal",
    "valor_unitario_usd_por_t_1998", "produccion_mundial_t",
]


def resolver_url_xlsx_vigente() -> str:
    resp = requests.get(URL_LANDING, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    m = re.search(r'href="(https://[^"]+ds140-copper-\d{4}\.xlsx)"', resp.text)
    if not m:
        raise RuntimeError(
            "No se encontró un enlace .xlsx en la página de USGS — el formato de la "
            "página pudo haber cambiado. Revisar manualmente: " + URL_LANDING
        )
    return m.group(1)


def procesar_dataframe(df: pd.DataFrame, url_xlsx: str, extraido_utc: str | None = None) -> dict:
    """Función pura (sin red ni disco): recibe el DataFrame ya leído de la
    hoja 'Copper' y devuelve el diccionario de resultado. Aislada del I/O
    para poder testear con un DataFrame pequeño construido a mano en
    `tests/test_phase8_usgs_historia.py`, sin depender de un .xlsx real.
    """
    if "Year" not in df[0].values:
        raise ValueError(
            "No se encontró la fila de encabezado 'Year' en la columna 0 — "
            "el formato de la hoja 'Copper' pudo haber cambiado."
        )
    fila_encabezado = df[df[0] == "Year"].index[0]
    fecha_modificacion_m = re.search(r"Last modification: (.+)", str(df.iloc[3, 0]))

    datos = df.iloc[fila_encabezado + 1:].copy()
    datos = datos[pd.to_numeric(datos[0], errors="coerce").notna()]  # descarta filas de notas al pie
    if datos.empty:
        raise ValueError("No se encontraron filas de datos numéricos después del encabezado 'Year'.")
    datos[0] = datos[0].astype(int)

    serie = []
    for _, fila in datos.iterrows():
        registro = {"ano": int(fila[0])}
        for i, clave in enumerate(COLUMNAS, start=1):
            valor = fila[i]
            registro[clave] = None if pd.isna(valor) else (int(valor) if float(valor).is_integer() else float(valor))
        serie.append(registro)

    primero, ultimo = serie[0], serie[-1]

    return {
        "fuente": "USGS Data Series 140 — Historical Statistics for Mineral and Material Commodities in the United States, ficha de Copper",
        "url_pagina": URL_LANDING,
        "url_archivo_descargado": url_xlsx,
        "ultima_modificacion_reportada_por_usgs": fecha_modificacion_m.group(1) if fecha_modificacion_m else None,
        "extraido_utc": extraido_utc or datetime.now(timezone.utc).isoformat(),
        "unidad": "toneladas métricas (t) de contenido de cobre, salvo el valor unitario en USD/t",
        "cobertura_geografica": "Estados Unidos (excepto la columna 'produccion_mundial_t', que es global)",
        "rango_anos": [primero["ano"], ultimo["ano"]],
        "num_anos": len(serie),
        "primer_registro": primero,
        "ultimo_registro": ultimo,
        "serie_completa": serie,
    }


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PDF_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    url_xlsx = resolver_url_xlsx_vigente()
    nombre_archivo = url_xlsx.rsplit("/", 1)[-1]

    resp = requests.get(url_xlsx, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    ruta_local = PDF_CACHE_DIR / nombre_archivo
    ruta_local.write_bytes(resp.content)

    df = pd.read_excel(ruta_local, sheet_name="Copper", header=None)
    salida = procesar_dataframe(df, url_xlsx)

    with open(OUT_DIR / "usgs_ds140_copper_historia.json", "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    primero, ultimo = salida["primer_registro"], salida["ultimo_registro"]
    print(f"[Fase 8] Archivo: {nombre_archivo}")
    print(f"[Fase 8] Cobertura: {primero['ano']}-{ultimo['ano']} ({salida['num_anos']} años)")
    print(f"[Fase 8] Producción de EE. UU. {primero['ano']}: {primero['produccion_primaria_t']:,} t "
          f"→ {ultimo['ano']}: {ultimo['produccion_primaria_t']:,} t")
    print(f"[Fase 8] Producción mundial {primero['ano']}: {primero['produccion_mundial_t']:,} t "
          f"→ {ultimo['ano']}: {ultimo['produccion_mundial_t']:,} t")
    return 0


if __name__ == "__main__":
    sys.exit(main())
