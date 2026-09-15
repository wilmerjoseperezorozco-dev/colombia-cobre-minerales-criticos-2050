# ADR 002 — FRED como fuente del precio histórico del cobre (no Bloomberg/Reuters/LME)

- **Estado:** Aceptado
- **Fecha:** 2026-09-15 (decisión original tomada al construir la Fase 2; documentada formalmente aquí tras una revisión externa)

## Contexto

El pipeline necesita una serie histórica de precio del cobre, actualizada
en cada corrida, para calcular CAGR/volatilidad y darle contexto de mercado
a los hallazgos sobre potencial minero de Colombia. Las fuentes candidatas
evaluadas al construir la Fase 2 fueron:

| Fuente | Acceso | Costo | Autenticación |
|---|---|---|---|
| **FRED** (Federal Reserve Bank of St. Louis), serie `PCOPPUSDM` | CSV público, URL estable | Gratis | Ninguna (sin API key) |
| Bloomberg Terminal / API | Suscripción institucional | USD miles/año | Credenciales de licencia |
| Refinitiv/LSEG (ex-Reuters) Eikon | Suscripción institucional | USD miles/año | Credenciales de licencia |
| London Metal Exchange (LME) datos oficiales | API de pago para datos en tiempo real/histórico granular | De pago para lo útil (el nivel gratuito es limitado) | API key de pago |

## Decisión

Se eligió **FRED, serie PCOPPUSDM**, por estos criterios, en orden de peso:

1. **Sin barrera de acceso.** Este es un pipeline de investigación pública
   pensado para correr sin intervención humana cada semana vía GitHub
   Actions (ver `docs/09-metodologia-pipeline.md` sección 7). Cualquier
   fuente que requiera una clave de API pagada introduce una dependencia
   operativa (¿quién paga la suscripción? ¿qué pasa si vence?) que
   Bloomberg/Refinitiv no pueden resolver sin presupuesto institucional —
   inexistente para este proyecto en su fase actual.
2. **Dato primario, no revendido.** PCOPPUSDM es la serie de precio del
   cobre del **FMI (Fondo Monetario Internacional), Primary Commodity
   Prices**, republicada por FRED — no es una estimación de mercado
   secundaria. Esto importa: el propio dataset ya documenta un caso real
   de por qué esta distinción no es cosmética — el bloque
   `consenso_mercado_secundario_no_verificado_contra_fuente_primaria` en
   `data/consolidado/dataset_maestro.json` quedó marcado explícitamente
   como no verificado precisamente porque provenía de un resumen de
   prensa (S&P Global/Wood Mackenzie citados de forma imprecisa), no de la
   fuente primaria — el mismo problema que se evitó de raíz al elegir FRED
   para el precio.
3. **Conectividad verificada en vivo, no asumida.** Antes de construir la
   Fase 2 se confirmó que `https://fred.stlouisfed.org/graph/fredgraph.csv?id=PCOPPUSDM`
   responde con un CSV parseable directamente desde este entorno, sin
   necesidad de cuenta ni token — condición que Bloomberg/Refinitiv no
   cumplen bajo ningún escenario (siempre exigen sesión autenticada).
4. **Frecuencia suficiente para el caso de uso.** La serie es mensual, lo
   cual alcanza para CAGR a 5 años y volatilidad interanual — el pipeline
   no necesita granularidad intradía (que es donde LME sí tendría una
   ventaja real sobre FRED, pero irrelevante aquí).

## Por qué se trata como fase **bloqueante** (única fuente "en vivo" con ese estatus)

A diferencia de las Fases 5-9 (documentos que se re-publican con baja
frecuencia, semanas o meses), FRED se actualiza constantemente y es la
única fase donde "la fase corrió pero devolvió datos viejos sin avisar"
sería un fallo silencioso grave — el precio es un insumo central de varias
secciones de `docs/01-analisis-ampliado-2026-2050.md`. Por eso, si FRED
está caído (más allá de los 3 reintentos con backoff exponencial de
`pipeline/http_utils.py`), el pipeline se detiene en vez de seguir con un
precio potencialmente obsoleto — ver ADR 001 para el criterio general de
qué se marca bloqueante.

## Consecuencias

**Positivas:**
- Cero costo operativo, cero secreto que rotar o que se pueda filtrar
  accidentalmente (no hay `.env` para esta fase — ver
  `docs/09-metodologia-pipeline.md` sección 5).
- El dato es trazable a una fuente primaria citable (FMI), reforzando la
  credibilidad del repositorio de cara a una eventual cita por DOI
  (Zenodo).

**Negativas (aceptadas conscientemente):**
- Sin granularidad intradía ni datos de futuros/opciones — si una versión
  futura de este proyecto necesitara eso, FRED no alcanza y habría que
  reevaluar esta decisión (probablemente hacia una API gratuita de datos
  de commodities con más frecuencia, no directamente hacia Bloomberg/LME,
  que seguirían siendo desproporcionados en costo para el caso de uso).
- Un solo punto de fallo: no hay una fuente de respaldo automática si FRED
  cambia de URL o retira la serie. Mitigado parcialmente por los
  reintentos de `pipeline/http_utils.py`, no eliminado — un cambio
  estructural de FRED seguiría requiriendo intervención humana.
