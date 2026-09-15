# Sismicidad inducida: el riesgo que Quebradona comparte con El Teniente, y cómo otros países ya lo atacan

> Origen de este documento: una pregunta directa del usuario sobre si la minería y la extracción de hidrocarburos empeoran los terremotos. La respuesta corta es que no causan los terremotos tectónicos grandes (esos son de placas), pero sí generan su propia sismicidad — real, documentada, y en el caso de la minería subterránea profunda, ya mortal en la región. Ver también el riesgo #9 en [`docs/01-analisis-ampliado-2026-2050.md`](01-analisis-ampliado-2026-2050.md).
>
> **Nota de validación (14-sep-2026):** la propuesta de "gemelo digital" (sección 6) se verificó contra evidencia adicional después de escribirse por primera vez. El hallazgo de esa verificación **no invalida ninguna conclusión previa de este repositorio** — pero sí corrige una premisa incompleta de la primera versión de este mismo documento (que Colombia debía construir el monitoreo desde cero) y confirma, con una consulta técnica real, que la infraestructura de datos necesaria ya es interoperable internacionalmente. Ver sección 3 para el detalle completo de la corrección.

## 1. Dos fenómenos distintos — no confundirlos

| | Sismos tectónicos (placas) | Sismicidad inducida |
|---|---|---|
| Causa | Choque de placas Nazca-Suramérica, acumulación de energía en siglos | Actividad humana: extracción, inyección de fluidos, colapso de cavidades mineras |
| Magnitud típica | M6-9+ (el M7,4 de Colombia en ago-2026, o el M7,2/7,5 de Venezuela) | Generalmente M<5, con excepciones documentadas hasta M5,8 (Oklahoma) y M4,3 (El Teniente, Chile) |
| ¿La minería/el fracking lo causan? | No — verificado por verificadores de hechos colombianos tras el sismo de ago-2026 | Sí, por mecanismos bien documentados (secciones 2 y 3) |
| ¿Se puede mitigar? | No (es geología de fondo) | **Sí — con monitoreo, regulación y diseño de ingeniería, secciones 4-6** |

## 2. El caso que más debería importarle a Colombia: El Teniente, 31 de julio de 2025

Quebradona está diseñada, según el propio informe técnico de UPME (`data/upme_informe_cobre_hallazgos_curados.json`), con técnicas "muy similares a las aplicadas en los grandes proyectos de minería subterránea Chuquicamata y El Teniente". Esto no es una comparación retórica — es la referencia técnica explícita del proyecto colombiano más avanzado en desarrollo.

**Qué pasó:** el 31 de julio de 2025, a las 17:34 hrs, un evento sísmico inducido de **magnitud 4,3 Mw** (energía liberada: 6,9×10⁹ julios) causó el desprendimiento de una cuña de roca de ~60 toneladas en el sector Andesita de El Teniente. **6 trabajadores subcontratistas murieron, 9 resultaron heridos.**

**Lo que una investigación de agosto de 2026 encontró (no es un accidente sin aviso previo):**

- El sistema de monitoreo sísmico (indicador CFE/CFT) registró alertas los días 26-28 y 30 de julio, con el indicador cayendo bajo los parámetros normales.
- La mañana del 31 de julio, reportes operacionales ya documentaban "alta sismicidad" en los sectores Dacita Sur, Recursos Norte y Reno.
- A las 14:00 hrs, trabajadores en descanso reportaron explosiones "mucho más fuertes que las habituales" — 3,5 horas antes del colapso.
- **La cadena de mando decidió deliberadamente ignorar los umbrales de peligro**, permitiendo que contratistas entraran a sectores que, según los propios datos técnicos en tiempo real, debieron evacuarse de inmediato.
- En 2021, Codelco había retirado un "pilar de desacoplamiento" de 120 metros que el diseño aprobado en 2018 exigía como barrera de seguridad — convirtiendo, según el informe, "un diseño teóricamente seguro en una configuración de alto riesgo".
- Tras un colapso previo en 2023 en la misma intersección, las reparaciones fueron "locales y estáticas", sin reingeniería para responder a eventos de mayor magnitud.
- El procedimiento interno (P-03) permitía que un supervisor de turno declarara la sismicidad "fuera de rango" y simultáneamente autorizara operaciones sin restricción, sin un mecanismo de escalamiento obligatorio a especialistas.

**Por qué esto es Brumadinho con otro nombre:** el patrón es idéntico al que ya documentamos en `docs/06-soluciones-juridicas-e-institucionales.md` — advertencias técnicas reales, ignoradas por presión de producción, con una barrera de seguridad removida años antes por razones operativas. Solo cambia el mecanismo físico (relaves vs. sismicidad inducida).

**Consecuencia directa para Colombia:** si Quebradona replica las técnicas de El Teniente, replicar el proyecto sin replicar *también* un sistema de monitoreo sísmico independiente y con autoridad real de detener la operación (no solo asesorar) sería repetir el error, no la técnica.

## 3. Corrección importante: Colombia NO parte de cero — ya tiene un caso real, sin resolver, desde 2013

**Validación de esta propuesta (14-sep-2026):** al verificar la premisa de la sección 6 contra evidencia adicional, se encontró que Colombia ya tiene un antecedente real de sismicidad inducida — no hipotético, con casi 13 años de historia — que cambia el diagnóstico: **la propuesta de gemelo digital no es "construir algo que no existe", es generalizar y darle autoridad real a algo que ya opera de forma parcial y aislada.**

### 3.1 Puerto Gaitán, Meta (2013-presente)

- **Desde abril de 2013**, los campos petroleros Rubiales y Quifa (operados en ese momento por Pacific Rubiales, canadiense) registraron **más de 900 sismos** en la zona — frente a solo **11 eventos entre 1993 y 2013**.
- **Causa identificada:** ~95% de lo que se extrae de los pozos de producción es "agua de producción", que se reinyecta casi en su totalidad — en el momento más intenso, **~4 millones de barriles de agua al día**.
- **El SGC ya opera monitoreo sísmico local en tiempo real** en la zona, con una red de estaciones instaladas alrededor de los pozos — es decir, **el componente de monitoreo del gemelo digital propuesto ya existe, aislado, en este único sitio.**
- **El vacío regulatorio real y documentado:** cuando el Comité Ambiental de Puerto Gaitán (con apoyo de CAJAR) pidió ante el Tribunal de Cundinamarca suspender las reinyecciones como medida cautelar, **el Ministerio de Minas y Energía alegó que su regulación sobre sismicidad "no aplicaba a campos convencionales"** — es decir, la norma que sí existía solo cubría operaciones no convencionales (fracking), dejando fuera exactamente el mecanismo que causó los sismos de Puerto Gaitán. Este es el vacío específico que cualquier protocolo de semáforo colombiano debe cerrar explícitamente (ver sección 6).
- Existe además un estudio académico revisado por pares específicamente sobre este caso ("Seismicity induced by massive wastewater injection near Puerto Gaitán, Colombia"), lo que confirma que no es una percepción ciudadana sino un fenómeno estudiado científicamente.

### 3.2 La Guajira — reportado, sin confirmación oficial de causalidad

Existen reportes (no una confirmación oficial del SGC sobre la causalidad exacta) de un incremento fuerte de sismicidad en La Guajira: de 873 eventos registrados entre 1993-2017, **419 (49,7%) ocurrieron solo entre 2011-2017**, coincidiendo con actividad de prospección sísmica para gas/petróleo y minería de carbón a cielo abierto. Se reporta la asociación tal como aparece en la fuente, sin adoptarla como causalidad confirmada — a diferencia de Puerto Gaitán, que sí tiene estudio académico dedicado.

### 3.3 Validación técnica: la infraestructura de datos ya es interoperable internacionalmente

Se verificó en vivo (no se asumió) que la Red Sismológica Nacional de Colombia (RSNC, código de red `CM`, operada por el SGC) está registrada en la Federación Internacional de Redes Sismográficas Digitales (FDSN) con DOI propio (`10.7914/SN/CM`), y que sus metadatos de estaciones son consultables mediante el protocolo estándar internacional FDSNWS a través de la federación EarthScope/IRIS. Una consulta real devolvió, entre otras, estas estaciones:

| Estación | Ubicación | Relevancia para este repositorio |
|---|---|---|
| `CRJC` | Cerrejón, La Guajira (11,02 N / -72,88 W) | Activa desde nov-2014 — justo la zona de infraestructura pesada que `docs/11` identificó como candidata |
| `COD` | Agustín Codazzi, Cesar (9,94 N / -73,44 W) | Cerca de San Diego/La Paz, la zona de recurso de cobre real identificada en `docs/11` (activa 2011-2014, sin confirmar si sigue operativa) |

**Por qué esto importa para la propuesta:** el "gemelo digital" no requiere inventar una capa de interoperabilidad de datos — ya existe un estándar internacional funcionando, y Colombia ya lo usa. El trabajo real pendiente no es técnico de bajo nivel (protocolo de datos), es de integración institucional (cruzar esos datos con la telemetría operacional en tiempo real) y de gobernanza (darle autoridad de cierre real a lo que hoy es monitoreo pasivo).

## 4. Cómo otros países regulan la sismicidad inducida — comparación real

| País/región | Mecanismo regulado | Instrumento | Umbral de acción | Resultado documentado |
|---|---|---|---|---|
| **Oklahoma, EE. UU.** | Inyección de agua residual de petróleo/gas (no el fracking en sí) | Traffic Light Protocol (semáforo sísmico) | Amarillo M≥2,5 → reduce volumen de inyección; Rojo M≥4,0 → cierre inmediato del pozo | Pasó de 24 sismos M≥3/año (1973-2008) a 688 en 2014 (pico); las restricciones post-2016 (tras el M5,8, el más grande registrado) redujeron la sismicidad de forma medible |
| **Alberta, Canadá** | Fracturamiento hidráulico | Traffic Light Protocol | Amarillo ML1,5 → reevaluación obligatoria, informe al regulador, análisis de mitigación de riesgo | Aplicado tras el clúster sísmico de Fox Creek |
| **Reino Unido** | Fracturamiento hidráulico | Traffic Light Protocol (el más estricto del mundo) | Umbrales calibrados contra los sismos de Preston New Road | Contribuyó a la moratoria de fracking en Inglaterra |
| **Finlandia** | Estimulación de pozos geotérmicos profundos | Monitoreo sísmico casi en tiempo real | Control activo durante la estimulación de un pozo de 6,1 km cerca de Helsinki | Permitió controlar la sismicidad inducida durante la operación misma, no solo después |
| **Países Bajos (Groningen)** | Extracción de gas (mecanismo distinto: subsidencia, no inyección) | Reducción forzada de producción, luego cierre total | Ley de cierre total firmada abril de 2024, cierre completo planeado para 2030 | Miles de reclamos de compensación por daños a viviendas; **Shell y ExxonMobil demandan al Estado holandés por miles de millones en tribunales de arbitraje (ISDS) por el cierre** — ver sección 6 |
| **Chile (El Teniente)** | Minería subterránea de hundimiento de bloques | Monitoreo sísmico en mina + **fracturamiento hidráulico usado de forma proactiva** para preacondicionar la roca y reducir el riesgo de estallidos de roca | — | Técnica reconocida como efectiva para controlar sismicidad inducida por minería — pero el caso de jul-2025 (sección 2) muestra que la tecnología sin gobernanza real no basta |
| **Texas (Cuenca Pérmica), EE. UU.** | Volumen de agua residual a inyectar (reduce la causa raíz, no solo reacciona) | Reciclaje y reúso de agua de producción | — | 50-60% del agua de producción ya se recicla para nuevo fracturamiento (dato 2025); proyección de 80% para 2030; infraestructura de una sola empresa (Select Water Solutions) con capacidad de 3,4 millones de barriles/día |

**Lectura para Colombia:** ningún país "resolvió" la sismicidad inducida con una sola medida — combinan (1) reducir el volumen de fluido inyectado en origen (Texas), (2) un protocolo de semáforo con autoridad real de detener la operación (Oklahoma/Alberta/UK), y (3) mitigación de ingeniería activa en el caso de minería (Chile). Groningen es la advertencia de qué pasa cuando se actúa tarde: cierre total forzado, más una factura legal de miles de millones.

## 5. La palanca más barata: reducir el agua residual, no solo monitorear después

Si Colombia autoriza el fracking, la lección más aplicable y más barata de copiar es la de Texas: **la mayor parte del riesgo de sismicidad inducida por fracking no viene de fracturar la roca, viene de inyectar el agua residual sobrante en pozos de disposición profunda.** Reducir esa agua en origen reduce el riesgo en la fuente, no solo mejora la capacidad de reaccionar a tiempo:

- **Reciclaje y reúso directo:** tratar el agua de producción (membranas de ósmosis inversa, evaporación térmica, oxidación avanzada) para reutilizarla en el siguiente pozo de fracturamiento, en vez de inyectarla como desecho.
- **Reúso de beneficio ambiental:** Texas ya está desarrollando permisos para reúso agrícola o vertimiento a ríos de agua tratada a estándares más altos — más caro, pero reduce el volumen total que necesita disposición profunda.
- **Meta realista para Colombia si autoriza fracking:** exigir por regulación, desde el primer contrato, una meta de reciclaje de agua de producción (ej. 50% desde el año 1, siguiendo el punto de partida real de Texas), no dejarlo como buena práctica voluntaria.

## 6. Propuesta: generalizar el modelo de Puerto Gaitán, no construir uno nuevo

**Premisa corregida (ver sección 3):** la primera versión de esta propuesta asumía que Colombia debía construir el monitoreo de sismicidad inducida desde cero. Eso era incompleto — Colombia ya opera una versión local, aislada y sin autoridad de cierre en Puerto Gaitán desde 2013. La propuesta real es **generalizar ese modelo a nivel nacional, estandarizarlo, y darle la autoridad legal que hoy no tiene.**

**Lo que ya existe (verificado, no asumido):**
- El **Servicio Geológico Colombiano (SGC)** opera la Red Sismológica Nacional de Colombia (RSNC, red `CM`), registrada internacionalmente en la FDSN (DOI `10.7914/SN/CM`), con datos de estaciones accesibles vía protocolo estándar — confirmado con una consulta real (sección 3.3).
- **Un prototipo funcional de monitoreo local en tiempo real ya opera en Puerto Gaitán**, alrededor de los pozos Rubiales/Quifa, desde que empezó la crisis sísmica de 2013.
- Estaciones específicas ya activas en zonas de interés minero: `CRJC` en Cerrejón (La Guajira) y, históricamente, `COD` en Cesar.
- Un antecedente institucional de cooperación: el estudio conjunto SGC-MinEnergía "Estudio de Amenazas Sísmicas en el Sector Minero-Energético" (socializado el 22-nov-2024), con una guía metodológica de evaluación de geoamenaza ya publicada — la relación institucional para construir sobre ella ya existe.

**El vacío real a cerrar (no es tecnológico, es de gobernanza y alcance regulatorio):**

1. **Cerrar el vacío regulatorio de "campos convencionales":** el propio Ministerio de Minas y Energía alegó en 2016 que su regulación de sismicidad no cubría campos convencionales como Rubiales — cualquier norma nueva debe cubrir explícitamente inyección de agua en operaciones convencionales, no convencionales (fracking) y minería subterránea profunda, sin excepciones por tipo de operación.
2. **Generalizar el monitoreo de Puerto Gaitán** a Quebradona (antes de que entre en producción) y a cualquier bloque de fracking futuro, en vez de crear un monitoreo aislado por cada crisis según ocurra.
3. **Capa de datos unificada:** integrar la telemetría operacional de cada proyecto (volumen inyectado/extraído, presión, profundidad) con los datos sísmicos de la RSNC en tiempo real — hoy son sistemas que se cruzan caso por caso (como en Puerto Gaitán), no de forma sistemática nacional.
4. **Modelo de pronóstico con aprendizaje automático:** replicar la metodología ya documentada internacionalmente (modelos de pronóstico en tiempo real de sismicidad inducida, usados en almacenamiento geológico de CO2 y en pozos geotérmicos) para estimar la magnitud máxima esperable dado el ritmo de inyección/extracción actual.
5. **Protocolo de semáforo con autoridad real de cierre:** el caso de Puerto Gaitán muestra el problema exacto a resolver — cuando la comunidad pidió suspender la reinyección, tuvo que ir a un tribunal, porque no existía un mecanismo administrativo automático. El caso de El Teniente muestra el otro extremo — un supervisor de turno podía autorizar operación pese a sismicidad "fuera de rango". La solución que ningún país reseñado en la sección 4 tiene exactamente así: que el SGC (no el operador, no un juez, no el Ministerio) tenga la potestad técnica de activar el semáforo rojo, con acatamiento legal automático por ANM/ANH — combinando el monitoreo ya real de Colombia con la autoridad automática de Oklahoma/Alberta/UK.
6. **Panel público de transparencia:** el mismo principio de `docs/03-estudios-colombia-y-ejecucion.md` — un tablero abierto donde las comunidades vecinas (Puerto Gaitán ya vivió la alternativa: litigar a ciegas) puedan ver el nivel de alerta sísmica vigente sin necesidad de una acción judicial para conocerlo.

**Por qué esto es una síntesis genuinamente nueva, no una copia:** ningún país de la sección 4 combina exactamente (a) un prototipo de monitoreo local ya operando, (b) infraestructura de datos internacionalmente interoperable ya conectada, y (c) un vacío regulatorio ya documentado judicialmente — Colombia tiene los tres elementos simultáneamente, lo que hace que cerrar la brecha sea más barato aquí que en cualquiera de los países de referencia (que sí tuvieron que construir su capa de monitoreo desde cero).

**Fase realista de implementación:**
- **Meses 0-6:** convenio SGC-ANM-ANH que (a) formalice el intercambio de datos operacionales en tiempo real más allá del caso aislado de Puerto Gaitán, y (b) cierre por decreto el vacío regulatorio de "campos convencionales".
- **Meses 6-18:** extender el modelo de monitoreo de Puerto Gaitán a Quebradona antes de su entrada en producción, y calibrar el modelo de pronóstico con los 13 años de datos ya existentes de Puerto Gaitán (una ventaja de datos históricos que ningún piloto nuevo tendría).
- **Meses 18-36:** protocolo de semáforo con autoridad legal real, exigible como condición de licencia para Quebradona y cualquier proyecto futuro de fracking.

## 7. La lección contractual de Groningen que Colombia no puede permitirse ignorar

Cuando Países Bajos decidió cerrar el campo de gas de Groningen por el riesgo sísmico a la población, **Shell y ExxonMobil demandaron al Estado holandés por miles de millones de dólares en tribunales de arbitraje privados (ISDS)** — usando exactamente el tipo de protección que los tratados de inversión les garantizan.

**Por qué esto le importa a Colombia antes de firmar cualquier contrato de fracking o de minería subterránea profunda:** si el país necesita cerrar o restringir un proyecto por riesgo sísmico ya en marcha (como El Teniente debió haber hecho el 31 de julio de 2025 y no hizo), y el contrato no anticipó esa posibilidad, el Estado colombiano queda expuesto al mismo tipo de demanda que hoy enfrenta el gobierno holandés. **Recomendación concreta:** cualquier contrato futuro de fracking o de minería subterránea profunda en Colombia debe incluir, desde la firma, una cláusula explícita de suspensión o cierre por riesgo sísmico verificado por el SGC, sin que eso constituya expropiación indirecta ni active cláusulas de protección de inversión — blindando jurídicamente al Estado antes de que la decisión de cerrar sea necesaria, no después.

---
*Ver también: [Análisis ampliado 2026-2050](01-analisis-ampliado-2026-2050.md) · [Soluciones jurídicas e institucionales](06-soluciones-juridicas-e-institucionales.md) · [IA, medición y fórmulas](02-ia-medicion-y-formulas.md)*
