# Medir esto con IA: estudios, herramientas y fórmulas

## 1. Dos usos de la IA que importan a Colombia hoy

| Uso | Qué resuelve | Estado del arte (2026) | Aplicabilidad en Colombia |
|---|---|---|---|
| **Mapeo de prospectividad mineral (MPM)** | Dónde explorar en el 97% del territorio sin explorar | Random Forest, CNN, "deep forest" sobre datos geoquímicos + sensores remotos (Sentinel/Landsat) | Alta — UPME/SGC ya tienen mapas metalogénicos y geoquímicos departamentales como insumo base |
| **Monitoreo de relaves con IA + satélite** | Prevenir un Brumadinho/Mariana | InSAR (radar satelital, precisión milimétrica) + cámaras/sensores + algoritmos predictivos (ej. plataformas tipo VROC, SAP) | Alta — aplicable desde el diseño de cualquier nuevo proyecto (Quebradona, El Alacrán, ronda de 14 áreas) |

## 2. Mapeo de prospectividad mineral (MPM) — cómo funciona

**Insumos típicos (todos ya existen para Colombia, en distinto grado de completitud):**
- Mapas geoquímicos (Universidad Nacional ya generó los primeros mapas departamentales, incluyendo cobre, níquel, molibdeno).
- Mapa metalogénico de Colombia (UPME/SGC, base Sepúlveda Ospina et al., 2020).
- Imágenes de sensores remotos (Sentinel-2, Landsat) para alteración hidrotermal — indicador indirecto de pórfidos cupríferos.
- Datos geofísicos (magnetometría, gravimetría) cuando existen.

**Algoritmos usados en la literatura reciente (2023–2026):**
- Random Forest y Support Vector Machines: buen desempeño con muestras moderadas, alta interpretabilidad relativa.
- Redes neuronales convolucionales (CNN): mejor para patrones espaciales complejos en imágenes satelitales.
- "Deep forest" (ensamble de bosques profundos): usado específicamente para exploración de cobre pórfido a escala de sistema completo, combinando geología + sensores remotos.

**Limitaciones documentadas que Colombia enfrentaría igual que el resto del mundo:**
- Escasez de muestras etiquetadas (pocos depósitos confirmados para entrenar el modelo).
- Baja interpretabilidad de modelos profundos (difícil justificar ante inversionistas o comunidades por qué el modelo señala un área).
- Heterogeneidad de datos (mapas de distintas épocas y resoluciones).
- Capacidad limitada de generalizar de una región a otra (un modelo entrenado en los Andes peruanos no necesariamente funciona igual en el cinturón andino colombiano sin recalibración).

**Respaldo académico incorporado (25-sep-2026):** Li et al. (2026, *Chemical Geology*, [10.1016/j.chemgeo.2026.123659](https://doi.org/10.1016/j.chemgeo.2026.123659)) desarrollaron un modelo de machine learning interpretable para clasificar el tipo genético de un yacimiento (incluyendo pórfido cuprífero) a partir de la química de elementos traza de la calcopirita — el mineral de cobre más común de la corteza terrestre. Entrenado sobre 5.232 análisis de 232 depósitos a nivel mundial, alcanzó 0,96 de exactitud balanceada. Es la primera referencia académica revisada por pares que este repositorio incorpora sobre metodología de clasificación geológica asistida por IA aplicable directamente a exploración de cobre (no solo detección de alteración hidrotermal por sensores remotos, como se venía citando).

## 3. Monitoreo de relaves con IA — el estándar que Colombia debería exigir ya

- **InSAR (Interferometric Synthetic Aperture Radar):** monitorea desplazamiento del terreno con precisión milimétrica sobre toda la superficie de un dique de relaves y su entorno — detecta movimientos sutiles antes de que sean visibles.
- **Plataformas integradas (ej. tipo VROC, SAP):** combinan cámaras, sensores en sitio, satélite y drones con algoritmos predictivos para anticipar niveles de agua, drenaje, integridad estructural, actividad sísmica y polvo.
- **Cambio de paradigma:** de monitoreo reactivo (inspecciones periódicas, que fallaron en Brumadinho pese a estar "aprobadas") a control de riesgo proactivo con alertas tempranas automatizadas.
- **Recomendación operativa:** exigir por contrato, desde la ronda de 14 áreas en adelante, que todo nuevo proyecto de relaves incorpore InSAR + monitoreo continuo como condición de licencia, no como mejora voluntaria posterior.

**Respaldo académico incorporado (25-sep-2026) — hasta ahora esta sección solo citaba blogs especializados en tecnología, señalado como brecha en `docs/15-auditoria-rigor-evidencial.md`:**
- Sánchez et al. (2026, *Science of the Total Environment*, [10.1016/j.scitotenv.2025.181161](https://doi.org/10.1016/j.scitotenv.2025.181161)), con coautoría de investigadores en Ecuador (UTE University, Universidad Central del Ecuador) — revisión sistemática de InSAR diferencial multitemporal (DInSAR) para monitoreo de relaves: confirma que PSI, SBAS e ISBAS (las 3 técnicas InSAR principales) rinden mejor en condiciones distintas y que un uso híbrido mejora la detección, pero advierte que la estandarización sigue siendo limitada y que la adopción más amplia requiere apoyo regulatorio — un matiz que esta sección no tenía: InSAR no es un estándar único y maduro, es un campo todavía en consolidación.
- Hu et al. (2026, *Measurement*, [10.1016/j.measurement.2026.122237](https://doi.org/10.1016/j.measurement.2026.122237)) — modelo no supervisado (atención multi-cabeza + GRU) para detectar anomalías en la línea freática de un relave (el indicador más directo de riesgo de falla), con R²=0,937 y una tasa de alarma dinámica del 21,8% para cambios abruptos de corto plazo frente a solo 3,6% de falsas alarmas globales — evidencia concreta de que el "cambio de paradigma" hacia control proactivo mencionado arriba ya tiene una implementación técnica publicada, no es solo una aspiración.
- Fardin (2026, *Soil Dynamics and Earthquake Engineering*, [10.1016/j.soildyn.2026.110214](https://doi.org/10.1016/j.soildyn.2026.110214)) — análisis dinámico del relave de Fundão (Brasil, nov-2015, el otro gran desastre de relaves de la región junto a Brumadinho): encontró que la contribución sísmica al colapso fue **limitada** (los sismos de baja magnitud que precedieron la falla actuaron como disparador secundario, acelerando un proceso de licuefacción ya en curso por causas estáticas, no como causa principal). Esto matiza —sin contradecir— la narrativa de sismicidad inducida de `docs/12`: el mecanismo dominante en Fundão fue geotécnico-estático, distinto al de El Teniente, donde la sismicidad inducida sí fue el evento gatillante directo. No todo colapso de relave es, ante todo, un problema sísmico.

## 4. Fórmulas y métricas técnicas relevantes

### 4.1 Ley de corte (cutoff grade) y grado equivalente

Cuando un yacimiento tiene varios metales (ej. cobre + oro, como en Quebradona), se convierte el valor de los metales secundarios a un "grado equivalente" del metal principal para poder aplicar un único criterio de decisión:

```
Ley equivalente de cobre (%) = Ley_Cu + (Ley_metal_secundario × Precio_metal_secundario × Recuperación_secundario)
                                          ────────────────────────────────────────────────────────────────────
                                                    Precio_Cu × Recuperación_Cu
```

La ley de corte de equilibrio ("break-even cutoff grade") es aquella en la que el ingreso iguala el costo — por debajo de ella, procesar el mineral destruye valor.

### 4.2 Optimización por Valor Presente Neto (VPN/NPV)

La ley de corte óptima no es fija: es una función no lineal del VPN, porque el VPN depende de la ley de corte elegida y la ley de corte óptima depende a su vez del VPN esperado (algoritmo de Lane es la referencia clásica de la industria para resolver este problema).

```
VPN = Σ (Flujo de caja neto del año t) / (1 + tasa de descuento)^t   para t = 1 … vida útil de la mina
```

**Por qué importa para Colombia:** cualquier evaluación seria de Quebradona, El Alacrán o los proyectos de la ronda de 14 áreas debe presentar la ley de corte usada y su sensibilidad al precio del cobre (rango USD 8.000–13.500/t observado en 2026), no un único escenario optimista.

### 4.3 Intensidad de cobre por unidad de demanda futura (para dimensionar infraestructura)

```
Demanda proyectada de cobre (t) = Σ (unidades proyectadas de cada tecnología) × (intensidad de cobre por unidad)
```

Ejemplo con los datos ya capturados en [`/data/metricas_demanda_global_cobre.json`](../data/metricas_demanda_global_cobre.json):
- 1 vehículo eléctrico → 83 kg Cu
- 1 aerogenerador offshore → 4–15 t Cu
- 1 centro de datos de 300 MW → 6.000–9.000 t Cu

Esta fórmula simple permite a cualquier entidad colombiana traducir "cuántos data centers/VE/aerogeneradores se van a construir en el mundo" en "cuántas toneladas de cobre colombiano podrían venderse", ejercicio que hoy no aparece publicado por ninguna entidad estatal colombiana consultada.

## 5. Qué falta construir en Colombia (brecha de capacidad de medición)

No se encontró evidencia de un programa formal colombiano de mapeo de prospectividad con IA, ni de un estándar obligatorio de monitoreo de relaves con InSAR. Ambos son, con la evidencia recogida, las dos inversiones en "capacidad de medición" de mayor retorno por dólar invertido: no requieren esperar a que madure un proyecto minero (15 años) para generar valor — el mapeo de prospectividad genera valor apenas se identifican nuevos blancos de exploración, y el monitoreo de relaves genera valor (reducción de riesgo) desde el primer día de operación.

---
*Ver también: [Análisis ampliado 2026-2050](01-analisis-ampliado-2026-2050.md) · [Estudios en Colombia y ejecución](03-estudios-colombia-y-ejecucion.md)*
