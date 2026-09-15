"""
Tests de `pipeline/http_utils.py` — la utilidad de reintentos agregada en
respuesta a "si FRED está caído... ¿qué pasa?".

No se golpea la red real: se monkeypatchea `requests.get` con una función
falsa que falla N veces según el escenario, para verificar el CONTRATO real
(cuántas veces reintenta, y ante qué códigos NO reintenta) sin depender de
que un servidor externo esté caído en el momento justo de correr el test.
"""
import requests

from pipeline.http_utils import get_con_reintentos


class _RespuestaFalsa:
    def __init__(self, status_code):
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            error = requests.exceptions.HTTPError(f"status {self.status_code}")
            error.response = self
            raise error


def test_reintenta_ante_error_5xx_y_termina_en_exito(monkeypatch):
    """Simula un servidor que responde 503 dos veces y luego 200 — el
    llamador solo debería ver el resultado final exitoso, sin propagar
    la excepción de los intentos fallidos intermedios."""
    llamadas = {"n": 0}

    def get_falso(url, **kwargs):
        llamadas["n"] += 1
        if llamadas["n"] < 3:
            return _RespuestaFalsa(503)
        return _RespuestaFalsa(200)

    monkeypatch.setattr(requests, "get", get_falso)
    # wait_exponential real tardaría segundos reales entre intentos; para el
    # test no nos interesa medir el tiempo, solo el conteo de reintentos.
    resp = get_con_reintentos("https://ejemplo.invalido/datos", timeout=5)
    assert resp.status_code == 200
    assert llamadas["n"] == 3


def test_no_reintenta_ante_404_falla_en_el_primer_intento(monkeypatch):
    """Un 404 es un error de la URL/fuente, no transitorio — reintentar no
    lo arregla. Debe fallar de inmediato, con una sola llamada real."""
    llamadas = {"n": 0}

    def get_falso(url, **kwargs):
        llamadas["n"] += 1
        return _RespuestaFalsa(404)

    monkeypatch.setattr(requests, "get", get_falso)
    try:
        get_con_reintentos("https://ejemplo.invalido/no-existe", timeout=5)
        assert False, "debía lanzar HTTPError"
    except requests.exceptions.HTTPError:
        pass
    assert llamadas["n"] == 1


def test_agota_los_3_intentos_y_relanza_si_nunca_se_recupera(monkeypatch):
    """Si el error transitorio (timeout) persiste en los 3 intentos, se
    relanza la excepción real — no se traga el fallo ni se inventa un
    resultado vacío."""
    llamadas = {"n": 0}

    def get_falso(url, **kwargs):
        llamadas["n"] += 1
        raise requests.exceptions.Timeout("se agotó el tiempo de espera")

    monkeypatch.setattr(requests, "get", get_falso)
    try:
        get_con_reintentos("https://ejemplo.invalido/lento", timeout=5)
        assert False, "debía lanzar Timeout tras agotar los reintentos"
    except requests.exceptions.Timeout:
        pass
    assert llamadas["n"] == 3
