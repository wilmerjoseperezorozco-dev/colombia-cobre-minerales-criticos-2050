"""
FASE 7 — Extracción y parseo del informe técnico UPME sobre cobre en Colombia.

Fuente:
  UPME, Subdirección de Minería — "Informe Cobre" (documento técnico de
  ~95 páginas, el más denso en tablas de recursos/reservas de todos los
  documentos de UPME identificados en docs/05-fuentes.md).
  URL: https://docs.upme.gov.co/SIMEC/SIMCO/Cifras-Sectoriales/EstudiosPublicaciones/Informe_Cobre_subdireccion_VD.pdf

Nota de infraestructura (hallazgo en sí mismo):
  La URL indexada por buscadores y citada en la bibliografía del propio
  documento (`www1.upme.gov.co/...`) NO RESUELVE en DNS público — se
  verificó con una consulta DNS-over-HTTPS a Google (Status NXDOMAIN). El
  dominio operativo real de UPME migró a `docs.upme.gov.co` (WordPress,
  detectado por cabecera `X-Redirect-By`). Este script usa la URL que
  efectivamente responde HTTP 200, no la URL "oficial" citada en la
  bibliografía — un ejemplo concreto y verificado de la brecha de acceso a
  datos oficiales colombianos documentada en `docs/03-estudios-colombia-y-ejecucion.md`.

Qué extrae automáticamente (texto tabular limpio, sin rotación):
  - Tabla 1: estimación de recursos hipotéticos del USGS por región geológica
    con influencia en Colombia (la fuente real de la cifra "9.7 / 37.3 Mt").
  - Tablas 2-8: recursos y reservas de los 5 proyectos con informes bajo
    estándares internacionales (El Roble, Quebradona, Soto Norte, Mocoa,
    San Matías/El Alacrán).

Qué NO se intenta auto-parsear (y por qué):
  La Tabla 28 (comparativo de impactos económicos, página 87) tiene
  encabezados de columna rotados 90° que pdfplumber extrae con el texto
  invertido caracter por caracter (ej. "nóiccudorP" en vez de "Producción").
  Auto-parsear esto con regex sería frágil y propenso a error silencioso.
  Esas cifras, junto con la sección narrativa de aspectos favorables/
  desfavorables y las conclusiones/recomendaciones oficiales de UPME, se
  transcribieron a mano con cita de página exacta en
  `data/upme_informe_cobre_hallazgos_curados.json` (origen
  `curado_investigacion_humana`, no `api_publica_en_vivo`).

Salida:
  data/live/upme_recursos_reservas_proyectos.json
  pipeline/_out/upme_informe_cobre_subdireccion.pdf (copia cruda, auditoría)
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pdfplumber

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
from pipeline.http_utils import get_con_reintentos  # noqa: E402

OUT_DIR = REPO_ROOT / "data" / "live"
PDF_CACHE_DIR = REPO_ROOT / "pipeline" / "_out"

URL = "https://docs.upme.gov.co/SIMEC/SIMCO/Cifras-Sectoriales/EstudiosPublicaciones/Informe_Cobre_subdireccion_VD.pdf"
URL_BIBLIOGRAFICA_CITADA_PERO_ROTA = "http://www1.upme.gov.co/simco/Cifras-Sectoriales/Paginas/inter-cobre.aspx"


def descargar_pdf() -> bytes:
    resp = get_con_reintentos(URL, timeout=40)
    return resp.content


def normalizar(texto: str) -> str:
    return re.sub(r"\s+", " ", texto).strip()


def parsear_potencial_nacional(texto_paginas: list[str]) -> dict:
    """Tabla 1: recursos hipotéticos del USGS por región con influencia en Colombia.

    Corrige una interpretación errónea que se había propagado en este mismo
    repositorio (ver docs/09-metodologia-pipeline.md, sección de correcciones):
    "9.7 Mt de un total de 37.3 Mt" trataba 37.3 Mt como si fuera el total del
    cinturón andino atribuible a Colombia. El texto original dice que 37.3 Mt
    es el PROMEDIO de tres regiones COMPARTIDAS con Ecuador, Perú e incluso
    Panamá (filas 1-3), mientras que Colombia tiene DOS regiones propias con
    7.7 Mt y 9.7 Mt de recursos hipotéticos cada una (filas 4-5) — un total
    específico de Colombia de 17.4 Mt, no 9.7 Mt.
    """
    texto = normalizar(" ".join(texto_paginas))

    m_promedio = re.search(
        r"estiman recursos hip[oó]t[eé]ticos de mineral de cobre de ([\d.]+) millones de toneladas",
        texto,
    )
    m_colombia = re.search(
        r"se estima un potencial ([\d.]+) y ([\d.]+) millones de toneladas de recursos hip[oó]t[eé]ticos",
        texto,
    )
    m_hectareas = re.search(
        r"declarar una superficie de ([\d,]+) hect[aá]reas como [aá]reas estrat[eé]gicas para mineral de cobre",
        texto,
    )

    # Cada fila de la Tabla 1 quedó partida por pdfplumber: el bloque de texto
    # de una "Plate" incluye, en orden intercalado, sus 4 valores numéricos Y
    # el código de tracto alfanumérico (ej. "005pCu1005") en posiciones
    # variables — reflejo de columnas PDF que se linealizan de forma distinta
    # según si el nombre de la región ocupa 1 o 2 líneas. Se extrae primero el
    # bloque completo de cada "Plate", y de ahí los números que NO sean parte
    # de un código alfanumérico (excluyendo dígitos pegados a letras).
    patron_bloque = re.compile(
        r"Plate (\d+), Porphyry Copper Assessment for Tract\s+(.*?)(?=Plate \d+, Porphyry|Fuente:)"
    )
    patron_numero_aislado = re.compile(r"(?<![a-zA-Z0-9])\d+(?:\.\d+)?(?![a-zA-Z0-9])")
    patron_tracto = re.compile(r"(005pCu\d+)")

    filas = []
    for m in patron_bloque.finditer(texto):
        plate, resto = m.group(1), m.group(2)
        numeros = patron_numero_aislado.findall(resto)
        tracto = patron_tracto.search(resto)
        if len(numeros) < 4:
            continue  # fila no parseable con este patrón — se omite, no se inventa un valor
        filas.append({
            "plate": int(plate),
            "codigo_tracto_usgs": tracto.group(1) if tracto else None,
            "recursos_estimados_in_situ_mt": float(numeros[0]),
            "probabilidad_recursos_in_situ_pct": int(float(numeros[1])),
            "recursos_economicos_promedio_mt": float(numeros[2]),
            "probabilidad_recursos_economicos_pct": int(float(numeros[3])),
        })

    return {
        "fuente_original": "USGS Assessment of Undiscovered Copper Resources of the World, 2015 (Scientific Investigations Report 2018-5160, v1.1, mayo 2019), citado por UPME",
        "correccion_metodologica": (
            "37.3 Mt es el PROMEDIO de recursos hipotéticos de 3 regiones geológicas COMPARTIDAS "
            "entre Colombia, Ecuador, Perú y/o Panamá (no exclusivas de Colombia). Colombia tiene "
            "además 2 regiones propias con 7.7 Mt y 9.7 Mt respectivamente. El potencial específico "
            "de Colombia (sumando sus 2 regiones propias) es de 17.4 Mt, no 9.7 Mt como se citó "
            "inicialmente en este mismo repositorio a partir de un resumen de prensa impreciso."
        ),
        "promedio_regiones_compartidas_mt": float(m_promedio.group(1)) if m_promedio else None,
        "potencial_colombia_propio_mt": (
            [float(m_colombia.group(1)), float(m_colombia.group(2))] if m_colombia else None
        ),
        "potencial_colombia_propio_total_mt": (
            round(float(m_colombia.group(1)) + float(m_colombia.group(2)), 1) if m_colombia else None
        ),
        "area_recomendada_reserva_estrategica_hectareas": (
            int(m_hectareas.group(1).replace(",", "")) if m_hectareas else None
        ),
        "detalle_por_region_usgs": filas,
    }


def extraer_bloque(texto_paginas: list[str], inicio_regex: str, fin_regex: str) -> str:
    texto = "\n".join(texto_paginas)
    m_inicio = re.search(inicio_regex, texto)
    if not m_inicio:
        return ""
    m_fin = re.search(fin_regex, texto[m_inicio.end():])
    fin = m_inicio.end() + m_fin.start() if m_fin else len(texto)
    return texto[m_inicio.start():fin]


def num(token: str):
    token = token.replace(",", "").strip()
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return None


def parsear_el_roble(texto_paginas: list[str]) -> dict:
    # La etiqueta de cada categoría queda partida por pdfplumber ALREDEDOR de
    # su fila de números (ej. "Recursos [1.039.200 4.34 2.29 ...] Medidos"),
    # reflejo de una celda de tabla PDF envuelta en dos líneas. El patrón
    # busca la palabra ancla que abre la fila, captura los 5 valores, y
    # verifica la palabra de cierre esperada.
    bloque = normalizar(extraer_bloque(texto_paginas, r"Tabla 2\. Recursos proyecto el Roble", r"2\.2\.2\."))
    filas = {}
    for categoria, apertura, cierre in [
        ("recursos_medidos", "Recursos", "Medidos"),
        ("recursos_indicados", "Recursos", "Indicados"),
        ("medidos_mas_indicados", "Medidos", r"\+Indicados"),
        ("recursos_inferidos", "Recursos", "Inferidos"),
    ]:
        patron = rf"{apertura}\s+([\d,]+)\s+([\d.]+)\s+([\d.]+)\s+([\d,]+)\s+([\d,]+)\s+{cierre}"
        m = re.search(patron, bloque)
        if m:
            filas[categoria] = {
                "mena_t": num(m.group(1)),
                "cu_pct": float(m.group(2)),
                "au_g_t": float(m.group(3)),
                "cu_lb_contenido": num(m.group(4)),
                "au_oz_contenido": num(m.group(5)),
            }
    return {
        "proyecto": "El Roble", "operador": "Atico Mining Corporation", "departamento": "Chocó",
        "fecha_corte_estimacion": "2020-09-30",
        "fuente": "Atico Mining, Technical Report 2021 (citado por UPME, Tabla 2)",
        "recursos": filas,
    }


def parsear_quebradona(texto_paginas: list[str]) -> dict:
    bloque = normalizar(extraer_bloque(texto_paginas, r"Tabla 3\. Recursos Minerales", r"2\.2\.3\."))
    recursos = {}
    for categoria, patron in [
        ("indicados", r"Indicados\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)"),
        ("inferidos", r"Inferidos\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)"),
    ]:
        m = re.search(patron, bloque)
        if m:
            recursos[categoria] = {
                "mena_mt": num(m.group(1)), "cu_pct": float(m.group(2)), "au_g_t": float(m.group(3)),
                "ag_g_t": float(m.group(4)), "mo_ppm": float(m.group(5)),
            }
    m_reservas = re.search(
        r"Probables\s+([\d,]+)\s+([\d.]+)\s+([\d.]+)\s+([\d,]+)\s+([\d,]+)", bloque
    )
    reservas = None
    if m_reservas:
        reservas = {
            "categoria": "probables", "mena_t": num(m_reservas.group(1)), "cu_pct": float(m_reservas.group(2)),
            "au_g_t": float(m_reservas.group(3)), "cu_contenido_t": num(m_reservas.group(4)),
            "au_contenido_oz": num(m_reservas.group(5)),
        }
    return {
        "proyecto": "Quebradona", "operador": "AngloGold Ashanti", "departamento": "Antioquia",
        "fuente": "Minera de Cobre Quebradona, 2019 (citado por UPME, Tablas 3-4)",
        "recursos": recursos, "reservas": reservas,
    }


def parsear_soto_norte(texto_paginas: list[str]) -> dict:
    bloque = normalizar(extraer_bloque(texto_paginas, r"Tabla 5\. Recursos proyecto Soto Norte", r"2\.2\.4\."))
    recursos = {}
    for categoria, patron in [
        ("indicados", r"Indicados\s+([\d,]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)"),
        ("inferidos", r"Inferidos\s+([\d,]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)"),
    ]:
        m = re.search(patron, bloque)
        if m:
            recursos[categoria] = {
                "mena_kt": num(m.group(1)), "cu_pct": float(m.group(2)), "au_g_t": float(m.group(3)),
                "ag_g_t": float(m.group(4)), "cu_contenido_klb": num(m.group(5)),
                "au_contenido_koz": num(m.group(6)), "ag_contenido_koz": num(m.group(7)),
            }
    m_reservas = re.search(
        r"Probables\s+([\d,]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", bloque
    )
    reservas = None
    if m_reservas:
        reservas = {
            "categoria": "probables", "mena_t": num(m_reservas.group(1)), "cu_pct": float(m_reservas.group(2)),
            "au_g_t": float(m_reservas.group(3)), "ag_g_t": float(m_reservas.group(4)),
            "cu_contenido_klb": num(m_reservas.group(5)), "au_contenido_koz": num(m_reservas.group(6)),
            "ag_contenido_koz": num(m_reservas.group(7)),
        }
    return {
        "proyecto": "Soto Norte", "operador_al_momento_del_informe": "Sociedad Minera de Santander (MINESA / Mubadala Investment Company)",
        "operador_2026_segun_prensa": "Aris Mining (adquirió participación mayoritaria posteriormente — ver docs/05-fuentes.md)",
        "departamento": "Santander",
        "fuente": "Sociedad Minera de Santander, 2016-2017 (citado por UPME, Tablas 5-6)",
        "recursos": recursos, "reservas": reservas,
    }


def parsear_mocoa(texto_paginas: list[str]) -> dict:
    bloque = normalizar(extraer_bloque(texto_paginas, r"Tabla 7\. Recurso Proyecto Mocoa", r"2\.2\.5\."))
    m = re.search(
        r"Inferidos\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", bloque
    )
    recursos = None
    if m:
        recursos = {
            "categoria": "inferidos", "mena_mt": num(m.group(1)), "cueq_pct": float(m.group(2)),
            "cu_pct": float(m.group(3)), "mo_pct": float(m.group(4)),
            "cueq_contenido_blbs": float(m.group(5)), "cu_contenido_blbs": float(m.group(6)),
            "mo_contenido_mlbs": float(m.group(7)),
        }
    return {
        "proyecto": "Mocoa Cobre-Molibdeno", "operador": "Libero Copper & Gold Corp.", "departamento": "Putumayo",
        "fuente": "Mocoa Copper-Molybdenum project technical report (citado por UPME, Tabla 7)",
        "recursos": recursos,
    }


def parsear_san_matias(texto_paginas: list[str]) -> dict:
    bloque = normalizar(extraer_bloque(texto_paginas, r"Tabla 8\. Recursos Indicados e Inferidos proyecto San Mat", r"3\. PRINCIPALES"))
    recursos = {}
    for categoria, patron in [
        ("indicados", r"Indicados\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)"),
        ("inferidos", r"Inferidos\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)"),
    ]:
        m = re.search(patron, bloque)
        if m:
            recursos[categoria] = {
                "mena_mt": float(m.group(1)), "cu_pct": float(m.group(2)), "au_g_t": float(m.group(3)),
                "ag_g_t": float(m.group(4)), "cu_contenido_t": num(m.group(5)),
                "au_contenido_oz": num(m.group(6)), "ag_contenido_oz": num(m.group(7)),
            }
    return {
        "proyecto": "San Matías (incluye el depósito El Alacrán, Montiel East, Montiel West y Costa Azul)",
        "operador_en_el_informe_2019": "Córdoba Minerals Corp.",
        "operador_2026_segun_prensa": "CMH Colombia / JCHX Mining Management (China) — Cordoba Minerals vendió su participación en may-2025, ver data/proyectos_cobre_colombia.json",
        "departamento": "Córdoba (Puerto Libertador)",
        "fuente": "NI 43-101 Technical Report and Resource Estimate, San Matías Copper-Gold-Silver Project, 2019 (citado por UPME, Tabla 8)",
        "recursos": recursos,
        "nota": "El Alacrán es uno de los 4 depósitos del proyecto San Matías, no un proyecto independiente — aclara la aparente duplicidad de nombres entre fuentes de prensa (que usan 'El Alacrán') y UPME (que usa 'San Matías').",
    }


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PDF_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    contenido = descargar_pdf()
    ruta_pdf = PDF_CACHE_DIR / "upme_informe_cobre_subdireccion.pdf"
    ruta_pdf.write_bytes(contenido)

    with pdfplumber.open(ruta_pdf) as pdf:
        textos = [p.extract_text() or "" for p in pdf.pages]

    potencial = parsear_potencial_nacional(textos[8:13])
    proyectos = {
        "el_roble": parsear_el_roble(textos[13:20]),
        "quebradona": parsear_quebradona(textos[19:24]),
        "soto_norte": parsear_soto_norte(textos[22:27]),
        "mocoa": parsear_mocoa(textos[23:27]),
        "san_matias": parsear_san_matias(textos[24:28]),
    }

    salida = {
        "fuente": "UPME, Subdirección de Minería — Informe Cobre",
        "url_efectivamente_usada": URL,
        "url_citada_en_bibliografia_del_documento_pero_no_resuelve_dns": URL_BIBLIOGRAFICA_CITADA_PERO_ROTA,
        "extraido_utc": datetime.now(timezone.utc).isoformat(),
        "num_paginas_documento": len(textos),
        "potencial_nacional_cobre": potencial,
        "recursos_y_reservas_por_proyecto": proyectos,
    }

    with open(OUT_DIR / "upme_recursos_reservas_proyectos.json", "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    print(f"[Fase 7] Documento UPME: {len(textos)} páginas procesadas")
    print(f"[Fase 7] Potencial Colombia (corregido): {potencial.get('potencial_colombia_propio_total_mt')} Mt "
          f"(regiones propias: {potencial.get('potencial_colombia_propio_mt')})")
    print(f"[Fase 7] Filas de la Tabla 1 (USGS) parseadas: {len(potencial.get('detalle_por_region_usgs', []))}/5")
    for clave, datos in proyectos.items():
        n_recursos = len(datos.get("recursos") or {}) if isinstance(datos.get("recursos"), dict) else (1 if datos.get("recursos") else 0)
        print(f"[Fase 7]   {datos['proyecto']}: {n_recursos} categorías de recursos parseadas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
