"""
FASE 9 — Auditoría de los 2 documentos de UPME restantes (no parseados a profundidad).

Por qué "auditoría" y no "extracción" (honestidad sobre el alcance):
  Estos dos documentos suman 402 páginas (240 + 162), frente a las 95 del
  Informe Cobre que la Fase 7 sí parsea tabla por tabla. Intentar extraer
  cada tabla de 402 páginas con el mismo nivel de detalle no es
  proporcional al valor esperado: una inspección manual de ambos
  documentos durante la construcción de esta fase confirmó que son
  mayormente análisis social/demográfico por municipio (población,
  pobreza, salud, educación) — la misma naturaleza de datos ya cubierta
  cualitativamente en docs/07-blindaje-social-barranquilla.md.

  Lo que SÍ aporta valor real y es proporcional al esfuerzo: catalogar
  TODAS las tablas de ambos documentos (número, página, título) y
  clasificarlas por tema, para que una revisión manual futura sepa
  exactamente dónde mirar si necesita algo específico — en vez de tener
  que releer 402 páginas de nuevo. Las tablas clasificadas como
  "recursos_reservas" o "economico_financiero" se destacan como
  prioritarias porque son las únicas categorías con posibilidad real de
  contener cifras no capturadas todavía por la Fase 7.

Fuentes:
  - Documento_Cobre_29-12-2023.pdf (UPME, 240 págs.)
  - Definitivo_Caracterizacion_de_aspectos_sociales_y_ambientales_pry_min_cobre_Colombia_2025.pdf (UPME, 162 págs.)

Salida:
  data/live/upme_auditoria_documentos_adicionales.json
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
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

DOCUMENTOS = [
    {
        "id": "documento_cobre_2023",
        "titulo": "Análisis social, ambiental y económico de los principales proyectos de minería de cobre en Colombia (2023)",
        "url": "https://docs.upme.gov.co/SIMEC/SIMCO/Cifras-Sectoriales/EstudiosPublicaciones/Documento_Cobre_29-12-2023.pdf",
        "archivo_local": "upme_documento_cobre_2023.pdf",
    },
    {
        "id": "caracterizacion_2025",
        "titulo": "Caracterización de aspectos sociales y ambientales en proyectos mineros de cobre en Colombia (2025)",
        "url": "https://docs.upme.gov.co/SIMEC/SIMCO/Cifras-Sectoriales/EstudiosPublicaciones/Definitivo_Caracterizacion_de_aspectos_sociales_y_ambientales_pry_min_cobre_Colombia_2025.pdf",
        "archivo_local": "upme_caracterizacion_cobre_2025.pdf",
    },
]

# Tablas ya capturadas por la Fase 7 (Informe Cobre) — para no marcar como
# "candidato nuevo" algo que, por título, es evidentemente lo mismo ya extraído.
PALABRAS_YA_CUBIERTAS = [
    "recursos proyecto el roble", "recursos minerales", "reservas",
    "recursos proyecto soto norte", "recurso proyecto mocoa",
    "recursos indicados e inferidos proyecto san mat",
    "resumen comparativo impactos económicos", "empleo anual comparativo",
    "estimación de recursos en zonas con influencia en colombia",
]

PALABRAS_CLAVE_POR_CATEGORIA = {
    # Orden intencional: las categorías más específicas se revisan primero
    # para evitar falsos positivos (ej. "recurso hídrico" no es un recurso
    # mineral, aunque contenga la palabra "recurso").
    "ambiental": ["ambiental", "hídric", "recurso hídrico", "runap", "biodiversidad",
                  "vertimiento", "residuo", "relave", "cola", "agua", "licencia"],
    "demografico_social": ["población", "pobreza", "salud", "educaci", "vivienda",
                            "víctimas", "natalidad", "mortalidad", "conflicto armado", "etnia", "étnic"],
    "economico_financiero": ["inversión", "empleo", "regalías", "renta", "ingreso",
                              "costo", "pib", "impuesto", "producto interno bruto"],
    "recursos_reservas": ["recursos minerales", "recursos y reservas", "reservas de",
                           "recursos indicados", "recursos medidos", "recursos inferidos",
                           "tenor", "ley de cu", "%cu", "potencial de mineral de cobre",
                           "recurso proyecto", "recursos proyecto"],
}


def clasificar_tabla(titulo: str) -> str:
    titulo_lower = titulo.lower()
    for palabra in PALABRAS_YA_CUBIERTAS:
        if palabra in titulo_lower:
            return "ya_cubierta_por_fase_7"
    for categoria, palabras in PALABRAS_CLAVE_POR_CATEGORIA.items():
        if any(p in titulo_lower for p in palabras):
            return categoria
    return "otro_sin_clasificar"


def asegurar_pdf_local(doc: dict) -> Path:
    ruta = PDF_CACHE_DIR / doc["archivo_local"]
    if not ruta.exists():
        resp = get_con_reintentos(doc["url"], headers=HEADERS, timeout=60)
        PDF_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        ruta.write_bytes(resp.content)
    return ruta


def catalogar_tablas(ruta_pdf: Path) -> tuple[list[dict], int]:
    tablas = []
    with pdfplumber.open(ruta_pdf) as pdf:
        num_paginas = len(pdf.pages)
        for i, pagina in enumerate(pdf.pages, start=1):
            texto = pagina.extract_text() or ""
            for m in re.finditer(r"Tabla (\d+)\.\s*([^\n]{1,140})", texto):
                numero, titulo = m.group(1), m.group(2).strip()
                # Descarta entradas de la "Lista de tablas" (índice): usan
                # líderes de puntos seguidos del número de página, ej.
                # "...título... ........... 47"
                if re.search(r"\.{3,}\s*\d+\s*$", titulo):
                    continue
                tablas.append({
                    "numero": int(numero),
                    "pagina": i,
                    "titulo": titulo,
                    "categoria": clasificar_tabla(titulo),
                })
    return tablas, num_paginas


DEPARTAMENTOS_PIB = [
    {"departamento": "Chocó", "proyecto_asociado": "El Roble"},
    {"departamento": "Antioquia", "proyecto_asociado": "Quebradona"},
    {"departamento": "Putumayo", "proyecto_asociado": "Mocoa Cobre-Molibdeno"},
    {"departamento": "Córdoba", "proyecto_asociado": "San Matías (El Alacrán)"},
    {"departamento": "Santander", "proyecto_asociado": "Soto Norte"},
]


def extraer_pib_mineria_por_departamento(ruta_pdf: Path, tablas_catalogadas: list[dict]) -> list[dict]:
    """Extrae la fila 'Explotación de minas y canteras' de la tabla de PIB
    departamental por sector, para los 5 departamentos con proyectos de cobre.

    Formato de la tabla en el PDF: 'Sector | Actividad Económica | 2019 | 2020
    | 2021 | 2022', con valores en porcentaje. UPME no aclara explícitamente
    en el propio texto de la tabla si el porcentaje es participación en el
    PIB departamental o en el PIB nacional de esa actividad — se transcribe
    el valor tal cual, sin inferir la base de cálculo (ver 'nota_interpretacion').

    El número de tabla de "PIB por departamento" difiere entre la edición 2023
    y la 2025 del documento (ej. Putumayo es la Tabla 72 en 2023 pero la 71 en
    2025) — por eso se busca por nombre del departamento en el título, no por
    número de tabla fijo.
    """
    resultados = []
    with pdfplumber.open(ruta_pdf) as pdf:
        for dep in DEPARTAMENTOS_PIB:
            fila_tabla = next(
                (t for t in tablas_catalogadas
                 if "producto interno bruto" in t["titulo"].lower()
                 and dep["departamento"].lower() in t["titulo"].lower()),
                None,
            )
            if not fila_tabla:
                continue
            pagina_idx = fila_tabla["pagina"] - 1
            texto = re.sub(r"\s+", " ", pdf.pages[pagina_idx].extract_text() or "")
            m = re.search(
                r"Explotaci[oó]n de minas y canteras\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)",
                texto,
            )
            if not m:
                continue
            valores = [float(v.replace(",", ".")) for v in m.groups()]
            resultados.append({
                "departamento": dep["departamento"],
                "proyecto_asociado": dep["proyecto_asociado"],
                "tabla_fuente": fila_tabla["numero"],
                "pagina": fila_tabla["pagina"],
                "explotacion_minas_y_canteras_pct_2019_2022": dict(zip(["2019", "2020", "2021", "2022"], valores)),
            })
    return resultados


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    resultado_documentos = []

    for doc in DOCUMENTOS:
        ruta_pdf = asegurar_pdf_local(doc)
        tablas, num_paginas = catalogar_tablas(ruta_pdf)

        # Deduplicar por número de tabla (una tabla referenciada en texto y
        # repetida como encabezado real puede aparecer dos veces)
        vistos = set()
        tablas_unicas = []
        for t in tablas:
            clave = (t["numero"], t["titulo"])
            if clave not in vistos:
                vistos.add(clave)
                tablas_unicas.append(t)

        candidatas_prioritarias = [
            t for t in tablas_unicas
            if t["categoria"] in ("recursos_reservas", "economico_financiero")
        ]

        pib_mineria = extraer_pib_mineria_por_departamento(ruta_pdf, tablas_unicas)

        resultado_documentos.append({
            "id": doc["id"],
            "titulo": doc["titulo"],
            "url": doc["url"],
            "num_paginas": num_paginas,
            "num_tablas_encontradas": len(tablas_unicas),
            "tablas_prioritarias_para_revision_manual": candidatas_prioritarias,
            "conteo_por_categoria": {
                cat: sum(1 for t in tablas_unicas if t["categoria"] == cat)
                for cat in set(t["categoria"] for t in tablas_unicas)
            },
            "pib_explotacion_minas_y_canteras_por_departamento": {
                "nota_interpretacion": "Porcentaje tal como aparece en la tabla fuente de UPME/DANE; el documento no aclara explícitamente si es participación en el PIB departamental o en el PIB nacional de esa actividad — no inferido, transcrito literal.",
                "datos": pib_mineria,
            },
            "catalogo_completo": tablas_unicas,
        })

    salida = {
        "nota_metodologica": (
            "Auditoría por catálogo, no extracción profunda — ver docstring de "
            "pipeline/phase9_upme_auditoria/audit_upme_docs_adicionales.py. Las tablas "
            "en 'tablas_prioritarias_para_revision_manual' son candidatas a contener "
            "cifras no capturadas todavía; el resto son mayormente análisis social/"
            "demográfico por municipio, ya cubierto cualitativamente en el repositorio."
        ),
        "procesado_utc": datetime.now(timezone.utc).isoformat(),
        "documentos": resultado_documentos,
    }

    with open(OUT_DIR / "upme_auditoria_documentos_adicionales.json", "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    for doc in resultado_documentos:
        print(f"[Fase 9] {doc['id']}: {doc['num_paginas']} páginas, {doc['num_tablas_encontradas']} tablas catalogadas")
        print(f"[Fase 9]   Por categoría: {doc['conteo_por_categoria']}")
        print(f"[Fase 9]   Prioritarias para revisión manual: {len(doc['tablas_prioritarias_para_revision_manual'])}")
        for t in doc["tablas_prioritarias_para_revision_manual"][:10]:
            print(f"[Fase 9]     - Tabla {t['numero']} (p.{t['pagina']}, {t['categoria']}): {t['titulo']}")
        for pib in doc["pib_explotacion_minas_y_canteras_por_departamento"]["datos"]:
            print(f"[Fase 9]     PIB minería {pib['departamento']} ({pib['proyecto_asociado']}): "
                  f"{pib['explotacion_minas_y_canteras_pct_2019_2022']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
