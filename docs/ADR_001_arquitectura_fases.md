# ADR 001 — Arquitectura por fases independientes, con bloqueo selectivo

- **Estado:** Aceptado
- **Fecha:** 2026-09-15
- **Contexto de la decisión:** revisión externa sobre resiliencia del pipeline ("¿qué pasa si una fuente cambia o cae?")

## Contexto

El pipeline consolida datos de 6 familias de fuentes completamente distintas
(FRED, USGS ×2, IEA, UPME ×2, y 4 páginas HTML de entidades colombianas sin
API), cada una con su propio formato (CSV, PDF, Excel, HTML), su propia
cadencia de publicación, y su propio nivel de fiabilidad de acceso. No hay
forma de tratarlas de manera uniforme sin perder honestidad sobre cuáles
fallan de forma aceptable y cuáles no.

## Decisión

El pipeline se organiza en **fases independientes**, cada una:
1. Vive en su propia carpeta (`pipeline/phaseN_*/`), con su propio script
   ejecutable de forma aislada (`python pipeline/phaseN_x/script.py` corre
   sin depender de que otra fase haya corrido antes).
2. Escribe su propia salida en `data/live/*.json`, nunca lee la salida de
   otra fase (excepto la Fase 4, que consolida al final).
3. Se declara explícitamente **bloqueante** o **no bloqueante** en
   `pipeline/run_pipeline.py` (ver tabla abajo) — la clasificación no es
   pareja "todo bloquea" ni "nada bloquea", es por fase, a propósito.

| Fase | Bloqueante | Por qué |
|---|---|---|
| 1 — Validación del seed | Sí | Si el dataset curado a mano no valida contra su schema, todo lo demás construye sobre datos rotos. |
| 2 — Precio FRED | Sí | Es la única fase con datos verdaderamente "en vivo" (cambia cada corrida); un fallo silencioso aquí dejaría el precio desactualizado sin que nadie lo note — mejor que el pipeline se detenga y lo señale. |
| 3 — Snapshot fuentes colombianas | No | Ver ADR de por qué el detalle completo, es solo un sensor de cambios, no una fuente de cifras — su fallo no invalida nada más. |
| 5, 6, 7, 8, 9 — USGS/IEA/UPME | No | Cada una parsea un documento (PDF/Excel) cuyo formato puede cambiar de edición a edición sin aviso. Un cambio de formato no es un error del pipeline, es un evento a revisar — no debe tumbar las demás fases que sí funcionan. |
| 4 — Consolidación | Sí | Necesita que exista al menos el resultado de las fases 1 y 2 para producir un dataset mínimamente coherente. |
| Auditoría semanal | No | Es observabilidad (ver ADR pendiente sobre detección de anomalías), no validación — una alerta se reporta, no bloquea. |
| Guardrail final | Sí | Es la última línea de defensa lógica antes de publicar el dataset; si falla, el dataset no debe darse por bueno. |

## Qué pasa si una entidad colombiana (ANM/UPME/SGC/ANLA) agrega una API real mañana

Hoy, la Fase 3 hace snapshot + hash SHA-256 de HTML porque **no existe**
ninguna API pública de estas 4 entidades para minería de cobre (verificado
explícitamente, no asumido — ver `docs/09-metodologia-pipeline.md` sección
3). Si eso cambiara:

1. **No se modificaría la Fase 3 in situ** — se archivaría como referencia
   histórica (sigue siendo útil: detecta cuándo el sitio HTML se actualiza,
   independientemente de que exista una API en paralelo) y se crearía una
   **fase nueva** (`phase10_anm_api/` o similar, siguiendo el patrón de
   numeración por orden de incorporación, no de ejecución).
2. Esa fase nueva se construiría con el mismo patrón ya probado en las
   Fases 5-9: función pura de parseo (`parsear_respuesta_api(json_crudo)
   -> dict`) separada de la función de I/O (`descargar()`), para poder
   testearla con un fixture de respuesta real sin pegarle a la red en cada
   corrida de CI — exactamente como se hizo con `tests/fixtures/usgs_mcs_copper_texto_real.py`.
3. Se clasificaría como **no bloqueante** al principio (igual que toda fase
   nueva sobre una fuente recién integrada, hasta acumular corridas
   suficientes para confiar en su estabilidad) y se promovería a
   bloqueante solo si el equipo decide que esa fuente es crítica para la
   validez del dataset — la Fase 2 (FRED) es el único precedente de una
   fuente "en vivo" tratada como bloqueante, y fue una decisión explícita,
   no el default.
4. El guardrail de `pipeline/validaciones/validar_dataset_maestro.py` no
   necesitaría cambios de arquitectura — solo, potencialmente, una
   validación nueva si la API expone un campo que valga la pena
   contrastar contra otra fuente ya integrada (como ya se hace entre USGS
   y UPME para el potencial de Colombia).

## Consecuencias

**Positivas:**
- Un cambio de formato en un PDF de UPME (evento con precedente real en
  este mismo proyecto — ver la corrección de 9.7→17.4 Mt, causada por una
  interpretación imprecisa, no por un cambio de formato, pero de la misma
  familia de riesgo) no puede tumbar el precio del cobre ni la validación
  del dataset semilla.
- Cada fase es testeable y corrible en aislamiento — condición que ya se
  aprovechó para escribir 51+ tests sin necesitar red.

**Negativas (aceptadas conscientemente):**
- La clasificación bloqueante/no bloqueante es una decisión humana por
  fase, no derivada automáticamente de ninguna propiedad del código — un
  error de juicio al agregar una fase nueva (marcarla bloqueante cuando no
  debería, o viceversa) no lo detecta el sistema, lo detecta una revisión.
- No hay un grafo de dependencias declarativo entre fases (solo
  "antes/después de la 4") — ver la nota de roadmap en
  `docs/09-metodologia-pipeline.md` sobre cuándo esto se volvería
  insuficiente (Airflow/Prefect, no antes de que haga falta de verdad).
