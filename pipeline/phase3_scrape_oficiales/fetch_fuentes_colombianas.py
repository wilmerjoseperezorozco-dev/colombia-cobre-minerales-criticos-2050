"""
FASE 3 — Snapshot de fuentes oficiales colombianas (HTML público, sin API).

Realidad honesta de esta fase:
  ANM, UPME, ANLA y SGC publican información pública pero NO ofrecen una
  API estable ni datos abiertos estructurados para minería de cobre. Lo
  único automatizable de forma confiable es:
    1. Descargar el HTML público de páginas clave.
    2. Extraer el texto visible (sin tablas garantizadas, porque no las hay
       de forma consistente).
    3. Calcular un hash de contenido para detectar cuándo cambia la página
       entre una corrida del pipeline y la siguiente (útil para alertar
       "esto se movió, revisar a mano" en vez de fingir automatización
       total donde no existe).

  Esta fase NO reemplaza la investigación humana de las fases 1 y 4 — es
  un sensor de cambios, no un extractor de datos estructurados. Cualquier
  intento de "parsear" cifras específicas de estas páginas sin revisión
  humana sería poco confiable y se documenta así deliberadamente.

Salida:
  data/live/snapshots_fuentes_oficiales.json
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
from pipeline.http_utils import get_con_reintentos  # noqa: E402

OUT_DIR = REPO_ROOT / "data" / "live"
OUT_PATH = OUT_DIR / "snapshots_fuentes_oficiales.json"

FUENTES = [
    {"id": "anm_ronda_cobre", "url": "https://www.anm.gov.co/ronda-minera-cobre",
     "institucion": "Agencia Nacional de Minería (ANM)"},
    {"id": "anm_mapa_sitio_mineria", "url": "https://www.anm.gov.co/mapa-sitio-mineria-en-colombia",
     "institucion": "Agencia Nacional de Minería (ANM)"},
    {"id": "upme_home", "url": "https://www.upme.gov.co",
     "institucion": "Unidad de Planeación Minero-Energética (UPME)"},
    {"id": "sgc_home", "url": "https://www.sgc.gov.co",
     "institucion": "Servicio Geológico Colombiano (SGC)"},
    {"id": "anla_home", "url": "https://www.anla.gov.co",
     "institucion": "Autoridad Nacional de Licencias Ambientales (ANLA)"},
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; investigacion-cobre-colombia/1.0; +investigacion academica sin fines comerciales)"}


def extraer_texto_visible(html):
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    texto = soup.get_text(separator=" ", strip=True)
    return " ".join(texto.split())


def cargar_snapshots_previos():
    if OUT_PATH.exists():
        with open(OUT_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"historial": {}}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    estado = cargar_snapshots_previos()
    historial = estado.get("historial", {})

    resultados = []
    for fuente in FUENTES:
        entrada = {
            "id": fuente["id"],
            "institucion": fuente["institucion"],
            "url": fuente["url"],
            "consultado_utc": datetime.now(timezone.utc).isoformat(),
        }
        try:
            resp = get_con_reintentos(fuente["url"], headers=HEADERS, timeout=15)
            texto = extraer_texto_visible(resp.text)
            hash_actual = hashlib.sha256(texto.encode("utf-8")).hexdigest()

            hash_previo = historial.get(fuente["id"], {}).get("hash")
            cambio_detectado = hash_previo is not None and hash_previo != hash_actual

            entrada.update({
                "http_status": resp.status_code,
                "longitud_texto_caracteres": len(texto),
                "hash_sha256": hash_actual,
                "cambio_detectado_desde_ultima_corrida": cambio_detectado,
                "extracto_primeros_500_caracteres": texto[:500],
            })
            historial[fuente["id"]] = {"hash": hash_actual, "ultima_corrida_utc": entrada["consultado_utc"]}
        except requests.RequestException as e:
            entrada.update({"http_status": None, "error": str(e)})

        resultados.append(entrada)

    salida = {
        "nota_metodologica": (
            "Snapshot de texto visible de páginas públicas sin API estructurada. "
            "No sustituye la lectura humana de los documentos oficiales (PDFs de UPME/SGC "
            "citados en docs/05-fuentes.md); su función es detectar cambios entre corridas."
        ),
        "ultima_corrida_utc": datetime.now(timezone.utc).isoformat(),
        "fuentes": resultados,
        "historial": historial,
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    ok = sum(1 for r in resultados if r.get("http_status") == 200)
    print(f"[Fase 3] Fuentes consultadas: {len(resultados)} — OK: {ok}")
    for r in resultados:
        cambio = r.get("cambio_detectado_desde_ultima_corrida")
        estado_txt = "CAMBIÓ" if cambio else ("sin cambio" if cambio is not None else "primera corrida")
        print(f"  - {r['id']}: HTTP {r.get('http_status')} · {estado_txt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
