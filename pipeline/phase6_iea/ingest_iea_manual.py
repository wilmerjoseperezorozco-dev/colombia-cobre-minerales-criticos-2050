"""
FASE 6 — Ingesta manual del IEA Critical Minerals Data Explorer 2026 (Copper).

Por qué esta fase es "manual" y no una API en vivo (honestidad técnica):
  La IEA no ofrece una API pública ni una clave programática para este
  dataset a través de una cuenta gratuita — se verificó directamente en el
  sitio: el botón "Download supply & demand data behind the Critical
  Minerals Data Explorer 2026 edition" exige una sesión de navegador
  autenticada (usuario/contraseña), no un token de API. Automatizar esa
  descarga requeriría manejar credenciales, algo que este pipeline no hace
  por política. En su lugar, el usuario descarga el archivo una vez desde
  su propia cuenta y esta fase lo ingesta y normaliza — el mismo patrón
  honesto que la Fase 7 usa para las tablas no auto-parseables de UPME.

Fuente:
  IEA, Critical Minerals Data Explorer — edición 2026, archivo Excel oficial
  con datos de demanda (por escenario: Current Policies, Stated Policies,
  High Demand) y oferta minera "base case" (proyectos existentes y en
  construcción) para los minerales de la transición energética.

Aviso de licencia:
  Este archivo se descargó con la cuenta gratuita de IEA del usuario del
  repositorio. Los términos de licencia de IEA para cuentas gratuitas
  permiten uso personal/no comercial; el archivo se conserva en este
  repositorio PRIVADO únicamente para reproducibilidad del análisis. No
  redistribuir el archivo crudo si este repositorio deja de ser privado.

Entrada esperada:
  pipeline/_manual_uploads/IEA_Critical_Minerals_Dataset_2026.xlsx
  (si no existe, la fase se omite con un mensaje claro — no es bloqueante)

Salida:
  data/live/iea_critical_minerals_copper.json
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "data" / "live"
ARCHIVO_MANUAL = REPO_ROOT / "pipeline" / "_manual_uploads" / "IEA_Critical_Minerals_Dataset_2026.xlsx"

HOJA_DEMANDA = "1 Total demand for key minerals"
HOJA_OFERTA = "2 Total supply for key minerals"

ANOS_DEMANDA = [2030, 2035, 2040, 2045, 2050]
ANOS_OFERTA = [2025, 2030, 2035, 2040]


def hash_archivo(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extraer_demanda_cobre(path: Path) -> dict:
    """Filas 6-17 de la hoja de demanda: bloque de Copper.

    Estructura de columnas (fila 4 = años, fila 3 = nombre de escenario):
    col 1 = 2025 (línea base); cols 3-7 = Current Policies 2030-2050;
    cols 9-13 = Stated Policies 2030-2050; cols 15-19 = High Demand 2030-2050.
    """
    df = pd.read_excel(path, sheet_name=HOJA_DEMANDA, header=None)

    fila_base_2025 = float(df.iloc[16, 1])  # fila 16 = "Total demand", col 1 = 2025
    escenarios = {
        "current_policies_scenario": list(df.iloc[16, 3:8].astype(float)),
        "stated_policies_scenario": list(df.iloc[16, 9:14].astype(float)),
        "high_demand_scenario": list(df.iloc[16, 15:20].astype(float)),
    }
    otros_usos_2025 = float(df.iloc[15, 1])
    energia_2025 = float(df.iloc[14, 1])
    share_2025 = float(df.iloc[17, 1])

    return {
        "unidad": "kt (miles de toneladas)",
        "notas": "'Total energy technologies' = demanda ligada a tecnologías de transición energética (solar, eólica, VE, almacenamiento, redes, hidrógeno). 'Other uses' = el resto de la demanda global de cobre (construcción, electrónica general, etc.). 'Total demand' = suma de ambas.",
        "2025_linea_base": {
            "total_demanda": fila_base_2025,
            "energia_transicion": energia_2025,
            "otros_usos": otros_usos_2025,
            "participacion_energia_transicion_pct": round(share_2025 * 100, 1),
        },
        "total_demanda_por_escenario_kt": {
            "anos": ANOS_DEMANDA,
            **escenarios,
        },
    }


def extraer_oferta_cobre(path: Path) -> dict:
    """Filas 5-14 de la hoja de oferta: bloque 'Copper - Mining', base case."""
    df = pd.read_excel(path, sheet_name=HOJA_OFERTA, header=None)

    paises = {}
    for fila in range(6, 13):
        nombre_pais = df.iloc[fila, 0]
        if pd.isna(nombre_pais):
            continue
        valores = df.iloc[fila, 1:5].astype(float).tolist()
        paises[str(nombre_pais)] = dict(zip(ANOS_OFERTA, valores))

    total = df.iloc[13, 1:5].astype(float).tolist()
    top3 = df.iloc[14, 1:5].astype(float).tolist()

    return {
        "unidad": "kt (miles de toneladas), producción minera",
        "escenario": "base case (proyectos existentes + en construcción, sin nueva inversión) — NO es un escenario de demanda equivalente; representa el techo de oferta si no se aprueban proyectos nuevos",
        "anos": ANOS_OFERTA,
        "por_pais": paises,
        "total_mundial": dict(zip(ANOS_OFERTA, total)),
        "participacion_top3_paises_pct": [round(v * 100, 1) for v in top3],
        "nota_colombia": "Colombia no aparece como país individual — queda dentro de 'Rest of world', igual que en la tabla del USGS (ver data/live/usgs_copper_mcs.json).",
    }


def main() -> int:
    if not ARCHIVO_MANUAL.exists():
        print(f"[Fase 6] Archivo manual no encontrado en {ARCHIVO_MANUAL.relative_to(REPO_ROOT)} — fase omitida.")
        print("[Fase 6] Para activarla: descargar el dataset desde la cuenta IEA del usuario y colocarlo en esa ruta.")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    demanda = extraer_demanda_cobre(ARCHIVO_MANUAL)
    oferta = extraer_oferta_cobre(ARCHIVO_MANUAL)

    salida = {
        "fuente": "IEA, Critical Minerals Data Explorer, edición 2026 (archivo Excel oficial)",
        "metodo_de_obtencion": "aportado_manualmente_por_usuario — descargado desde su cuenta gratuita de IEA; no existe API pública equivalente (ver docstring de este script)",
        "archivo_origen": str(ARCHIVO_MANUAL.relative_to(REPO_ROOT)),
        "archivo_sha256": hash_archivo(ARCHIVO_MANUAL),
        "procesado_utc": datetime.now(timezone.utc).isoformat(),
        "aviso_licencia": "Dataset con cuenta gratuita de IEA. Uso personal/no comercial. No redistribuir el archivo crudo fuera de este repositorio privado.",
        "demanda_cobre": demanda,
        "oferta_minera_cobre_base_case": oferta,
    }

    with open(OUT_DIR / "iea_critical_minerals_copper.json", "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    print("[Fase 6] IEA Critical Minerals Data Explorer 2026 — Copper")
    print(f"[Fase 6] Demanda total 2025 (línea base): {demanda['2025_linea_base']['total_demanda']:.0f} kt")
    print(f"[Fase 6] Demanda 2050 (Stated Policies): {demanda['total_demanda_por_escenario_kt']['stated_policies_scenario'][-1]:.0f} kt")
    print(f"[Fase 6] Oferta minera mundial 2025 (base case): {oferta['total_mundial'][2025]:.0f} kt")
    print(f"[Fase 6] Oferta minera mundial 2040 (base case, sin nueva inversión): {oferta['total_mundial'][2040]:.0f} kt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
