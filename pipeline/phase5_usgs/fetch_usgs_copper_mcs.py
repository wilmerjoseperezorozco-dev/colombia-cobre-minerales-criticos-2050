"""
FASE 5 — Extracción en vivo del USGS Mineral Commodity Summaries (Copper).

Fuente:
  U.S. Geological Survey, Mineral Commodity Summaries — ficha de una página
  por commodity, publicada en un patrón de URL estable:
  https://pubs.usgs.gov/periodicals/mcs{año}/mcs{año}-copper.pdf

  Es un PDF de 2 páginas, no un CSV — pero a diferencia de las páginas HTML
  de la Fase 3, el USGS mantiene un formato tabular consistente año a año,
  lo que hace razonable parsearlo con reglas (no solo hacer snapshot).

Qué extrae:
  - Estadísticas de EE. UU. (producción de mina/refinería, precios COMEX/LME)
  - Producción mundial de mina y refinería por país + reservas
  - El hallazgo de la designación de "mineral crítico" (fecha exacta,
    referencia del Federal Register) — dato que no aparece en ninguna otra
    fuente ya integrada al pipeline.
  - Contexto de Colombia frente a las reservas mundiales (Colombia no
    aparece individualizada en esta tabla — queda dentro de "Other
    countries"; se calcula qué proporción representaría el potencial de
    UPME sobre esa cifra, de forma transparente y marcada como estimación).

Limitación reconocida:
  El parseo de la tabla de países se basa en el formato de texto lineal que
  entrega pdfplumber para la edición vigente al construir este script
  (Mineral Commodity Summaries, February 2026). Si el USGS cambia el diseño
  del PDF en una edición futura, el parseo de la tabla de países puede
  fallar — se valida explícitamente y se reporta en vez de fallar en
  silencio (ver `advertencias` en la salida).

Salida:
  data/live/usgs_copper_mcs.json
  pipeline/_out/mcs{año}-copper.pdf (copia cruda del PDF, para auditoría)
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pdfplumber
import requests

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "data" / "live"
PDF_CACHE_DIR = REPO_ROOT / "pipeline" / "_out"

ANO_EDICION = 2026
URL = f"https://pubs.usgs.gov/periodicals/mcs{ANO_EDICION}/mcs{ANO_EDICION}-copper.pdf"

# Países con línea de datos en la tabla "World Mine and Refinery Production and
# Reserves" del MCS de copper. Los valores "—" (guion largo) del PDF indican
# dato no aplicable/no reportado, no cero.
PAISES_TABLA = [
    "United States", "Australia", "Canada", "Chile", "China", "Congo (Kinshasa)",
    "Germany", "India", "Indonesia", "Japan", "Kazakhstan", "Korea, Republic of",
    "Mexico", "Peru", "Poland", "Russia", "Zambia", "Other countries",
]


def descargar_pdf() -> bytes:
    resp = requests.get(URL, timeout=30)
    resp.raise_for_status()
    return resp.content


def num(token: str):
    """Convierte un token de la tabla USGS a número; None si es '—' (no aplicable)."""
    token = token.strip()
    if token in ("—", "--", "-", ""):
        return None
    token = token.replace(",", "")
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return None


def normalizar_espacios(texto: str) -> str:
    """Colapsa saltos de línea y espacios múltiples a un solo espacio.

    Necesario porque pdfplumber conserva los saltos de línea del PDF, y una
    misma oración puede partirse a mitad de frase — las expresiones
    regulares sobre texto corrido (párrafos) deben operar sobre la versión
    normalizada; las tablas (una fila = una línea) se parsean sobre el
    texto original, donde el salto de línea sí es significativo.
    """
    return re.sub(r"\s+", " ", texto).strip()


def parsear_designacion_critica(texto: str) -> dict:
    texto_plano = normalizar_espacios(texto)
    m = re.search(
        r"On (\w+ \d{1,2}, \d{4}), the U\.S\. Final \d{4} List of Critical Minerals "
        r"was published in the Federal Register \(([^)]+)\)\.",
        texto_plano,
    )
    if not m:
        return {"encontrado": False}
    minerales_agregados = re.search(r"addition of ([^.]+?), based on", texto_plano)
    return {
        "encontrado": True,
        "fecha_texto_original": m.group(1),
        "referencia_federal_register": m.group(2),
        "minerales_agregados_en_esta_lista": minerales_agregados.group(1).strip() if minerales_agregados else None,
    }


def parsear_salient_statistics_eeuu(texto: str) -> dict:
    """Extrae la serie 2021-2025e de EE.UU. (producción, precios) de forma tolerante a espacios."""
    resultado = {}

    patrones = {
        "produccion_mina_recuperable_kt": r"Mine, recoverable\s+([\d,\s]+e?)",
        "refinacion_primaria_kt": r"Primary \(from ore\)\s+([\d,\s]+e?)",
        "refinacion_secundaria_kt": r"Secondary \(from scrap\)\s+([\d,\s]+e?)",
        "consumo_reportado_refinado_kt": r"Reported, refined copper\s+([\d,\s]+e?)",
        "precio_productor_eeuu_catodo_centavos_lb": r"U\.S\. producer, cathode \(COMEX \+ premium\)\s+([\d.\s]+)",
        "precio_comex_centavos_lb": r"COMEX, high-grade, first position\s+([\d.\s]+)",
    }
    anos = ["2021", "2022", "2023", "2024", "2025e"]
    for clave, patron in patrones.items():
        m = re.search(patron, texto)
        if m:
            valores = [num(v) for v in m.group(1).split()]
            resultado[clave] = dict(zip(anos, valores))
    return resultado


def parsear_tabla_mundial(texto: str) -> dict:
    """Parsea la tabla 'World Mine and Refinery Production and Reserves'."""
    filas = {}
    advertencias = []
    for pais in PAISES_TABLA:
        # Busca una línea que empiece con el nombre del país seguido de hasta 5 números/guiones
        patron = re.escape(pais) + r"\s+([\d,]+|—)\s+([\d,]+|—)\s+([\d,]+|—)\s+([\d,]+|—)\s+([\d,]+|—)"
        m = re.search(patron, texto)
        if not m:
            advertencias.append(f"No se pudo parsear la fila del país: {pais}")
            continue
        mina_2024, mina_2025e, refineria_2024, refineria_2025e, reservas = (
            num(g) for g in m.groups()
        )
        filas[pais] = {
            "produccion_mina_kt_2024": mina_2024,
            "produccion_mina_kt_2025e": mina_2025e,
            "produccion_refineria_kt_2024": refineria_2024,
            "produccion_refineria_kt_2025e": refineria_2025e,
            "reservas_kt": reservas,
        }

    m_total = re.search(
        r"World total \(rounded\)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", texto
    )
    total = None
    if m_total:
        mina_2024, mina_2025e, refineria_2024, refineria_2025e, reservas = (num(g) for g in m_total.groups())
        total = {
            "produccion_mina_kt_2024": mina_2024,
            "produccion_mina_kt_2025e": mina_2025e,
            "produccion_refineria_kt_2024": refineria_2024,
            "produccion_refineria_kt_2025e": refineria_2025e,
            "reservas_kt": reservas,
        }
    else:
        advertencias.append("No se pudo parsear la fila 'World total (rounded)'")

    return {"por_pais": filas, "mundo_total": total, "advertencias": advertencias}


def parsear_recursos_mundiales(texto: str) -> dict:
    texto_plano = normalizar_espacios(texto)
    m = re.search(
        r"identified resources contained ([\d.]+) billion tons of unextracted copper "
        r"\(([\d.]+) billion tons when past production of ([\d.]+) million tons is included\) "
        r"and undiscovered resources contained an estimated ([\d.]+) billion tons of copper",
        texto_plano,
    )
    if not m:
        return {"encontrado": False}
    return {
        "encontrado": True,
        "recursos_identificados_sin_extraer_billones_toneladas_cortas": float(m.group(1)),
        "recursos_identificados_incluyendo_produccion_pasada_billones_toneladas_cortas": float(m.group(2)),
        "produccion_pasada_millones_toneladas_cortas": float(m.group(3)),
        "recursos_no_descubiertos_estimados_billones_toneladas_cortas": float(m.group(4)),
        "nota_unidad": "Toneladas cortas (short tons) de EE. UU., tal como reporta el USGS textualmente — no confundir con toneladas métricas usadas en el resto del pipeline.",
    }


def contexto_colombia(tabla_mundial: dict) -> dict:
    reservas_mundiales_kt = (tabla_mundial.get("mundo_total") or {}).get("reservas_kt")
    reservas_otros_paises_kt = (tabla_mundial.get("por_pais") or {}).get("Other countries", {}).get("reservas_kt")
    potencial_upme_mt = 9.7  # UPME, ver data/potencial_colombia_y_retos.json
    potencial_upme_kt = potencial_upme_mt * 1000

    resultado = {
        "nota": (
            "El USGS no reporta a Colombia como línea individual en esta tabla; "
            "queda agregada dentro de 'Other countries'. Las proporciones siguientes "
            "son un cálculo propio, no una cifra publicada por USGS."
        ),
        "potencial_upme_mt_cu": potencial_upme_mt,
    }
    if reservas_mundiales_kt:
        resultado["pct_potencial_colombia_sobre_reservas_mundiales"] = round(
            100 * potencial_upme_kt / reservas_mundiales_kt, 3
        )
    if reservas_otros_paises_kt:
        resultado["pct_potencial_colombia_sobre_bolsa_otros_paises"] = round(
            100 * potencial_upme_kt / reservas_otros_paises_kt, 3
        )
    return resultado


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PDF_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    contenido_pdf = descargar_pdf()
    ruta_pdf = PDF_CACHE_DIR / f"mcs{ANO_EDICION}-copper.pdf"
    ruta_pdf.write_bytes(contenido_pdf)

    with pdfplumber.open(ruta_pdf) as pdf:
        texto_completo = "\n".join(p.extract_text() or "" for p in pdf.pages)

    designacion_critica = parsear_designacion_critica(texto_completo)
    salient_stats = parsear_salient_statistics_eeuu(texto_completo)
    tabla_mundial = parsear_tabla_mundial(texto_completo)
    recursos = parsear_recursos_mundiales(texto_completo)
    colombia = contexto_colombia(tabla_mundial)

    m_edicion = re.search(r"Mineral Commodity Summaries, (\w+ \d{4})", texto_completo)

    salida = {
        "fuente": "U.S. Geological Survey — Mineral Commodity Summaries (ficha de Copper)",
        "url": URL,
        "edicion_reportada_por_el_pdf": m_edicion.group(1) if m_edicion else None,
        "extraido_utc": datetime.now(timezone.utc).isoformat(),
        "designacion_mineral_critico_eeuu": designacion_critica,
        "estadisticas_eeuu_serie_2021_2025e": salient_stats,
        "produccion_y_reservas_mundiales": tabla_mundial,
        "recursos_mundiales_usgs_2015": recursos,
        "contexto_colombia_vs_usgs": colombia,
    }

    with open(OUT_DIR / "usgs_copper_mcs.json", "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    print(f"[Fase 5] USGS MCS {salida['edicion_reportada_por_el_pdf']} — copper")
    print(f"[Fase 5] Designación de mineral crítico detectada: {designacion_critica.get('encontrado')}")
    if designacion_critica.get("encontrado"):
        print(f"[Fase 5]   Fecha: {designacion_critica['fecha_texto_original']} "
              f"({designacion_critica['referencia_federal_register']})")
    n_paises = len(tabla_mundial["por_pais"])
    print(f"[Fase 5] Países parseados en tabla mundial: {n_paises}/{len(PAISES_TABLA)}")
    if tabla_mundial["advertencias"]:
        for a in tabla_mundial["advertencias"]:
            print(f"[Fase 5]   ADVERTENCIA: {a}")
    if colombia.get("pct_potencial_colombia_sobre_reservas_mundiales") is not None:
        print(f"[Fase 5] Potencial de Colombia (UPME) = "
              f"{colombia['pct_potencial_colombia_sobre_reservas_mundiales']}% de las reservas mundiales USGS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
