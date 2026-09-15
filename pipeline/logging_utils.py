"""
Logging estructurado y registro de ejecución (agregado 15-sep-2026).

Antes de esto, la única forma de depurar una corrida de GitHub Actions era
leer el log crudo de `print()` de la Action — sin niveles, sin timestamps,
sin un resumen consultable por máquina. Este módulo no reemplaza los
`print()` internos de cada fase (siguen ahí, sirven para lectura humana
rápida en consola) — agrega una CAPA por encima, a nivel de orquestador,
que sí es estructurada y queda persistida como artefacto.

Qué produce: `pipeline/_out/ejecucion_log.json`, con un registro por fase:
  {"fase": ..., "estado": "ok"|"fallo"|"omitida", "duracion_s": ...,
   "excepcion": null | "texto del traceback resumido", "timestamp_utc": ...}
"""
import json
import logging
import sys
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "pipeline" / "_out"
LOG_EJECUCION_PATH = OUT_DIR / "ejecucion_log.json"


def configurar_logging(nivel=logging.INFO) -> logging.Logger:
    """Configura el logger raíz del pipeline con formato consistente.
    Idempotente: si ya se configuró (ej. al correr un submódulo aislado
    para tests), no duplica handlers."""
    logger = logging.getLogger("pipeline")
    if logger.handlers:
        return logger
    logger.setLevel(nivel)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(handler)
    return logger


@dataclass
class ResultadoFase:
    fase: str
    estado: str  # "ok" | "fallo" | "omitida"
    duracion_s: float
    timestamp_utc: str
    excepcion: str | None = None


@dataclass
class RegistroEjecucion:
    """Acumula el resultado de cada fase durante una corrida del pipeline y
    lo persiste como JSON al final — con o sin fallos, para que una corrida
    de GitHub Actions que falló a mitad de camino deje evidencia de hasta
    dónde llegó, no solo el mensaje genérico de 'Action failed'."""
    resultados: list = field(default_factory=list)

    def registrar(self, fase: str, estado: str, duracion_s: float, excepcion: BaseException | None = None):
        texto_excepcion = None
        if excepcion is not None:
            texto_excepcion = "".join(
                traceback.format_exception(type(excepcion), excepcion, excepcion.__traceback__)
            )[-2000:]  # se trunca a los últimos 2000 caracteres -- suficiente para ubicar la causa
        self.resultados.append(ResultadoFase(
            fase=fase, estado=estado, duracion_s=round(duracion_s, 2),
            timestamp_utc=datetime.now(timezone.utc).isoformat(), excepcion=texto_excepcion,
        ))

    def guardar(self) -> Path:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        payload = {
            "generado_utc": datetime.now(timezone.utc).isoformat(),
            "resumen": {
                "total_fases": len(self.resultados),
                "ok": sum(1 for r in self.resultados if r.estado == "ok"),
                "fallo": sum(1 for r in self.resultados if r.estado == "fallo"),
                "omitida": sum(1 for r in self.resultados if r.estado == "omitida"),
                "duracion_total_s": round(sum(r.duracion_s for r in self.resultados), 2),
            },
            "fases": [
                {"fase": r.fase, "estado": r.estado, "duracion_s": r.duracion_s,
                 "timestamp_utc": r.timestamp_utc, "excepcion": r.excepcion}
                for r in self.resultados
            ],
        }
        with open(LOG_EJECUCION_PATH, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return LOG_EJECUCION_PATH


class Cronometro:
    """Context manager mínimo para medir duración de una fase sin ensuciar
    el código del orquestador con time.time() manual en cada punto."""

    def __enter__(self):
        self._inicio = time.time()
        return self

    def __exit__(self, *_):
        self.duracion_s = time.time() - self._inicio
