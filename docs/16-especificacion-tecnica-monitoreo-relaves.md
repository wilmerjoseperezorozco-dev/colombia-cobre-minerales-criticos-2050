# Especificación técnica de monitoreo de relaves: de la literatura académica a una condición de licencia exigible

> Este documento convierte los 3 papers académicos incorporados el 25-sep-2026 (`docs/05`, sección "IA aplicada a exploración y monitoreo minero") en un estándar concreto que se pueda exigir por contrato — no la recomendación genérica "usar InSAR" que tenía antes `docs/02`, sino parámetros, umbrales y arquitecturas con desempeño publicado y medible.

## 1. Por qué esto no es solo una buena práctica, es una condición mínima verificable

Un operador puede afirmar que "monitorea con IA" sin que eso signifique nada operativo. Este documento existe para que UPME, ANM o ANLA puedan exigir, en el pliego de condiciones de cualquier proyecto nuevo (empezando por la ronda de 14 áreas estratégicas), métricas concretas — no una promesa de tecnología.

## 2. Requisito 1: monitoreo geodésico por InSAR diferencial multitemporal (MT-DInSAR)

Basado en Sánchez et al. (2026, *Science of the Total Environment*, [10.1016/j.scitotenv.2025.181161](https://doi.org/10.1016/j.scitotenv.2025.181161)):

| Fase del proyecto | Técnica InSAR recomendada por la literatura | Por qué |
|---|---|---|
| Construcción / llenado inicial | PSI (Persistent Scatterer Interferometry) + ISBAS combinados | Mayor sensibilidad a deformación rápida y localizada en terreno recién removido, donde la coherencia radar es baja |
| Operación estable | SBAS (Small Baseline Subset) | Mejor para tendencias de deformación lenta y sostenida sobre superficies ya consolidadas |
| Cualquier fase, como validación cruzada | Integración con GNSS, piezómetros e inclinómetros in situ | La literatura es explícita: InSAR solo, sin instrumentación terrestre que lo valide, no es suficiente — reduce falsos positivos/negativos por umbrales de coherencia y desenvolvimiento de fase mal calibrados |

**Cláusula exigible sugerida:** "El operador debe reportar trimestralmente los resultados de monitoreo MT-DInSAR con la técnica apropiada a la fase del proyecto (tabla anterior), validados cruzadamente con al menos una fuente de instrumentación terrestre, con metodología y umbrales de coherencia documentados públicamente."

## 3. Requisito 2: detección de anomalías en la línea freática con umbrales de desempeño publicados

Basado en Hu et al. (2026, *Measurement*, [10.1016/j.measurement.2026.122237](https://doi.org/10.1016/j.measurement.2026.122237)):

- **Arquitectura de referencia:** modelo no supervisado (no requiere años de datos de falla etiquetados, que Colombia no tiene) basado en atención multi-cabeza + unidad recurrente con compuertas (GRU), con selección de variables por coeficiente de información máxima.
- **Desempeño publicado como umbral mínimo aceptable:** R² ≥ 0,93 en la predicción de la evolución espacio-temporal de la línea freática; RMSE ≤ 0,08 (en las unidades normalizadas del estudio original — el operador debe reportar el RMSE en las unidades reales de su instrumentación, con la metodología de normalización explícita).
- **Mecanismo de doble alarma (el elemento más aplicable de este paper):** un límite de control global estático (ancla la frontera de seguridad de largo plazo) **y** una ventana adaptativa dinámica (detecta cambios abruptos de corto plazo). En el estudio de referencia, la tasa de alarma estática se mantuvo en 3,64% (baja tasa de falsos positivos, robustez global) mientras que la dinámica llegó a 21,82% (alta sensibilidad a cambios locales abruptos) — el punto no es replicar esas cifras exactas, es que **un solo umbral de alarma no es defendible técnicamente** cuando la literatura ya demuestra que un sistema de doble umbral captura ambos tipos de riesgo.

**Cláusula exigible sugerida:** "El sistema de monitoreo de línea freática debe implementar un mecanismo de doble alarma (límite estático de largo plazo + ventana dinámica de corto plazo), con metodología de calibración documentada y sometida a auditoría externa anual."

## 4. Requisito 3: monitoreo geotécnico-estático, no solo sísmico

Basado en Fardin (2026, *Soil Dynamics and Earthquake Engineering*, [10.1016/j.soildyn.2026.110214](https://doi.org/10.1016/j.soildyn.2026.110214)) — ver también la corrección de `docs/12`, sección 2:

- El caso de Fundão demuestra que un sistema de monitoreo centrado únicamente en sismicidad (el foco natural después de estudiar El Teniente) **no habría anticipado ese colapso** — la causa dominante fue geotécnica-estática (licuefacción por extrusión lateral), con la sismicidad como acelerador secundario, no como causa.
- **Implicación exigible:** ningún proyecto colombiano (Quebradona, El Alacrán, los de la ronda de 14 áreas) debería poder satisfacer su requisito de monitoreo solo con sismómetros, sin importar cuán robusto sea ese componente. El Requisito 2 (línea freática) no es opcional ni sustituible por el monitoreo sísmico — son complementarios, cada uno cubre un mecanismo de falla distinto.

## 5. Tabla resumen — lo mínimo que un pliego de licitación debería exigir

| Componente | Exigible desde | Sustituible por | Referencia |
|---|---|---|---|
| MT-DInSAR (técnica según fase) | Diseño del proyecto | No — es la única cobertura de superficie completa, no puntual | Sánchez et al. 2026 |
| Doble alarma de línea freática | Antes de operación | No | Hu et al. 2026 |
| Monitoreo sísmico (si aplica hundimiento de bloques) | Antes de operación, si el método minero lo justifica | No sustituye al monitoreo geotécnico-estático | Ver `docs/12` |
| Validación cruzada con instrumentación terrestre | Continua | No | Sánchez et al. 2026 |

## 6. Límite honesto de esta especificación

Ninguno de los 3 papers usados aquí fue desarrollado ni validado específicamente sobre un relave colombiano — son evidencia de que estas técnicas funcionan y tienen umbrales de desempeño publicados en contextos comparables (Ecuador, China, Brasil), no una garantía de que los mismos números se repliquen exactamente en El Roble o Quebradona. La recomendación operativa es adoptar la arquitectura y el principio de doble validación, calibrando los umbrales numéricos con datos locales una vez el monitoreo esté instalado — no copiar las cifras publicadas como si fueran universales.

---
*Ver también: [IA, medición y fórmulas](02-ia-medicion-y-formulas.md) · [Sismicidad inducida y gemelo digital](12-sismicidad-inducida-y-gemelo-digital.md) · [Fuentes y estrategia de búsqueda](05-fuentes.md)*
