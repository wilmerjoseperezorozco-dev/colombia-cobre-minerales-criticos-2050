"""
FASE 4 — Consolidación: dataset maestro con procedencia (provenance) y métricas calculadas.

Qué hace:
  Une todo lo producido por las fases 1-3 (datos curados por investigación
  humana + precio de cobre en vivo de FRED + snapshots de fuentes oficiales)
  en un único archivo, marcando explícitamente el origen de cada bloque
  (curado / api_publica / snapshot_html) para que nunca se confunda una
  estimación razonada con un dato verificado en vivo.

  Además calcula métricas derivadas reproducibles (no opiniones):
    - CAGR del precio del cobre en la ventana de 5 años más reciente.
    - Volatilidad (desviación estándar) del último año vs. los últimos 5.

Salida:
  data/consolidado/dataset_maestro.json
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
LIVE_DIR = DATA_DIR / "live"
OUT_DIR = DATA_DIR / "consolidado"


def cargar_json(path):
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def calcular_cagr(valor_inicial, valor_final, anos):
    if valor_inicial <= 0 or anos <= 0:
        return None
    return round(((valor_final / valor_inicial) ** (1 / anos) - 1) * 100, 3)


def metricas_precio_cobre(serie_json):
    if not serie_json:
        return None
    serie = serie_json["serie_completa"]
    df = pd.DataFrame(serie)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha")

    fecha_final = df["fecha"].iloc[-1]
    fecha_ini_5a = fecha_final - pd.DateOffset(years=5)
    ventana_5a = df[df["fecha"] >= fecha_ini_5a]
    ventana_1a = df[df["fecha"] >= (fecha_final - pd.DateOffset(years=1))]

    cagr_5a = calcular_cagr(
        ventana_5a["precio_usd_por_tonelada"].iloc[0],
        ventana_5a["precio_usd_por_tonelada"].iloc[-1],
        5,
    )

    return {
        "cagr_5_anos_pct": cagr_5a,
        "volatilidad_desv_estandar_ultimo_ano": round(float(ventana_1a["precio_usd_por_tonelada"].std()), 2),
        "volatilidad_desv_estandar_5_anos": round(float(ventana_5a["precio_usd_por_tonelada"].std()), 2),
        "n_observaciones_5_anos": int(len(ventana_5a)),
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    proyectos = cargar_json(DATA_DIR / "proyectos_cobre_colombia.json")
    demanda_global = cargar_json(DATA_DIR / "metricas_demanda_global_cobre.json")
    potencial = cargar_json(DATA_DIR / "potencial_colombia_y_retos.json")
    estudios = cargar_json(DATA_DIR / "estudios_cientificos_colombia.json")
    kpis = cargar_json(DATA_DIR / "kpis_hoja_de_ruta_2026_2050.json")
    precio_fred = cargar_json(LIVE_DIR / "copper_price_fred.json")
    snapshots = cargar_json(LIVE_DIR / "snapshots_fuentes_oficiales.json")

    metricas_precio = metricas_precio_cobre(precio_fred)

    dataset_maestro = {
        "generado_utc": datetime.now(timezone.utc).isoformat(),
        "esquema_version": "1.0",
        "bloques": {
            "proyectos_cobre_colombia": {
                "origen": "curado_investigacion_humana",
                "confiabilidad": "alta — verificado contra prensa especializada y comunicados oficiales, con fecha de corte explícita",
                "datos": proyectos,
            },
            "demanda_global_cobre": {
                "origen": "curado_investigacion_humana",
                "confiabilidad": "media-alta — cifras de IEA/S&P/Wood Mackenzie citadas, divergentes entre sí por escenario (ver nota metodológica del archivo)",
                "datos": demanda_global,
            },
            "potencial_colombia_y_retos": {
                "origen": "curado_investigacion_humana",
                "confiabilidad": "alta para hechos verificables (UPME, prensa), media para estimaciones propias marcadas como tal",
                "datos": potencial,
            },
            "estudios_cientificos_colombia": {
                "origen": "curado_investigacion_humana",
                "confiabilidad": "alta — inventario de fuentes primarias con URL",
                "datos": estudios,
            },
            "kpis_hoja_de_ruta": {
                "origen": "estimacion_propia_razonada",
                "confiabilidad": "baja-media — hipótesis de planificación explícitamente marcada como no oficial",
                "datos": kpis,
            },
            "precio_cobre_serie_historica": {
                "origen": "api_publica_en_vivo",
                "confiabilidad": "alta — FRED/FMI, dato oficial actualizado en cada corrida del pipeline",
                "metricas_calculadas": metricas_precio,
                "datos": precio_fred,
            },
            "snapshots_fuentes_oficiales_colombia": {
                "origen": "snapshot_html_sin_api",
                "confiabilidad": "solo como sensor de cambios — no usar como fuente de cifras sin verificación humana",
                "datos": snapshots,
            },
        },
    }

    out_path = OUT_DIR / "dataset_maestro.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dataset_maestro, f, ensure_ascii=False, indent=2)

    print(f"[Fase 4] Dataset maestro generado en {out_path.relative_to(REPO_ROOT)}")
    print(f"[Fase 4] Bloques consolidados: {list(dataset_maestro['bloques'].keys())}")
    if metricas_precio:
        print(f"[Fase 4] CAGR cobre (5 años): {metricas_precio['cagr_5_anos_pct']}% anual")
    return 0


if __name__ == "__main__":
    sys.exit(main())
