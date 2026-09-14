"""
FASE 2 — Extracción en vivo de precio histórico del cobre (fuente pública real).

Fuente:
  FRED (Federal Reserve Bank of St. Louis) — serie PCOPPUSDM
  "Global price of Copper" (USD por tonelada métrica, mensual, desde 1990).
  Endpoint CSV público, sin necesidad de API key:
  https://fred.stlouisfed.org/graph/fredgraph.csv?id=PCOPPUSDM

Por qué esta fuente y no otra:
  LME/COMEX no ofrecen series históricas gratuitas sin licencia. FRED
  republica la serie del FMI (Primary Commodity Prices) bajo dominio público,
  actualizada mensualmente, sin necesidad de credenciales — es la única
  fuente de precio de cobre verdaderamente abierta y estable que se
  verificó con conectividad real desde este entorno.

Salida:
  data/live/copper_price_fred.json   (serie completa + metadatos de origen)
  data/live/copper_price_fred.csv    (serie cruda tal cual llega de FRED)
"""
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "data" / "live"
URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=PCOPPUSDM"
SERIE_ID = "PCOPPUSDM"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    resp = requests.get(URL, timeout=20)
    resp.raise_for_status()
    csv_texto = resp.text

    with open(OUT_DIR / "copper_price_fred.csv", "w", encoding="utf-8") as f:
        f.write(csv_texto)

    df = pd.read_csv(io.StringIO(csv_texto))
    df.columns = ["fecha", "precio_usd_por_tonelada"]
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["precio_usd_por_tonelada"] = pd.to_numeric(df["precio_usd_por_tonelada"], errors="coerce")
    df = df.dropna().sort_values("fecha").reset_index(drop=True)

    ultimo = df.iloc[-1]
    fecha_final = pd.Timestamp(ultimo["fecha"])
    hace_5_anos = df[df["fecha"] >= (fecha_final - pd.DateOffset(years=5))]
    hace_1_ano = df[df["fecha"] >= (fecha_final - pd.DateOffset(years=1))]

    resultado = {
        "fuente": "FRED (Federal Reserve Bank of St. Louis) — serie PCOPPUSDM, origen FMI Primary Commodity Prices",
        "url": URL,
        "unidad": "USD por tonelada métrica",
        "frecuencia": "mensual",
        "extraido_utc": datetime.now(timezone.utc).isoformat(),
        "num_observaciones": int(len(df)),
        "rango_fechas": [df["fecha"].iloc[0].strftime("%Y-%m-%d"), df["fecha"].iloc[-1].strftime("%Y-%m-%d")],
        "ultimo_dato": {
            "fecha": fecha_final.strftime("%Y-%m-%d"),
            "precio_usd_por_tonelada": round(float(ultimo["precio_usd_por_tonelada"]), 2),
        },
        "estadisticas_ultimo_ano": {
            "promedio": round(float(hace_1_ano["precio_usd_por_tonelada"].mean()), 2),
            "minimo": round(float(hace_1_ano["precio_usd_por_tonelada"].min()), 2),
            "maximo": round(float(hace_1_ano["precio_usd_por_tonelada"].max()), 2),
        },
        "estadisticas_5_anos": {
            "promedio": round(float(hace_5_anos["precio_usd_por_tonelada"].mean()), 2),
            "minimo": round(float(hace_5_anos["precio_usd_por_tonelada"].min()), 2),
            "maximo": round(float(hace_5_anos["precio_usd_por_tonelada"].max()), 2),
        },
        "serie_completa": [
            {"fecha": f.strftime("%Y-%m-%d"), "precio_usd_por_tonelada": round(float(p), 2)}
            for f, p in zip(df["fecha"], df["precio_usd_por_tonelada"])
        ],
    }

    with open(OUT_DIR / "copper_price_fred.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"[Fase 2] Serie {SERIE_ID}: {resultado['num_observaciones']} observaciones "
          f"({resultado['rango_fechas'][0]} → {resultado['rango_fechas'][1]})")
    print(f"[Fase 2] Último dato: {resultado['ultimo_dato']['fecha']} = "
          f"USD {resultado['ultimo_dato']['precio_usd_por_tonelada']}/t")
    return 0


if __name__ == "__main__":
    sys.exit(main())
