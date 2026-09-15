"""
Utilidad compartida de descarga con reintentos (agregado 15-sep-2026, en
respuesta a una revisión externa: "si FRED está caído o USGS cambia el PDF
mañana, ¿qué pasa?" — antes de esto, la respuesta honesta era "la fase
falla en el primer intento, sin reintento, y punto").

Política de reintentos: 3 intentos con backoff exponencial (2s, 4s, 8s,
con un techo de 10s) SOLO ante errores transitorios (timeout, error de
conexión, o códigos 5xx/429 del servidor). Un 404 o un 403 NO se
reintenta — son errores de la fuente/URL, no transitorios, y reintentar no
los resuelve (ver `pipeline/logging_utils.py` para cómo queda registrado
un fallo, incluido el agotamiento de reintentos, en el log de ejecución).
"""
import logging

import requests
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger("pipeline.http")


def _es_error_transitorio(excepcion: BaseException) -> bool:
    if isinstance(excepcion, (requests.exceptions.Timeout, requests.exceptions.ConnectionError)):
        return True
    if isinstance(excepcion, requests.exceptions.HTTPError):
        response = excepcion.response
        return response is not None and (response.status_code == 429 or response.status_code >= 500)
    return False


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=10),
    retry=retry_if_exception(_es_error_transitorio),
    reraise=True,
)
def get_con_reintentos(url: str, **kwargs) -> requests.Response:
    """Reemplazo directo de `requests.get(url, **kwargs)` con reintentos
    automáticos ante fallos transitorios. `kwargs` acepta lo mismo que
    `requests.get` (headers, timeout, etc.) — el llamador sigue siendo
    responsable de pasar un `timeout` explícito, esta función no lo impone.
    """
    logger.debug("GET %s (intento con reintentos habilitado)", url)
    resp = requests.get(url, **kwargs)
    resp.raise_for_status()
    return resp
