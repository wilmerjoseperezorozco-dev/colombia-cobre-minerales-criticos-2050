# Sismicidad inducida: el riesgo que Quebradona comparte con El Teniente, y cómo otros países ya lo atacan

> Origen de este documento: una pregunta directa del usuario sobre si la minería y la extracción de hidrocarburos empeoran los terremotos. La respuesta corta es que no causan los terremotos tectónicos grandes (esos son de placas), pero sí generan su propia sismicidad — real, documentada, y en el caso de la minería subterránea profunda, ya mortal en la región. Ver también el riesgo #9 en [`docs/01-analisis-ampliado-2026-2050.md`](01-analisis-ampliado-2026-2050.md).

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

## 3. Cómo otros países regulan la sismicidad inducida — comparación real

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

## 4. La palanca más barata: reducir el agua residual, no solo monitorear después

Si Colombia autoriza el fracking, la lección más aplicable y más barata de copiar es la de Texas: **la mayor parte del riesgo de sismicidad inducida por fracking no viene de fracturar la roca, viene de inyectar el agua residual sobrante en pozos de disposición profunda.** Reducir esa agua en origen reduce el riesgo en la fuente, no solo mejora la capacidad de reaccionar a tiempo:

- **Reciclaje y reúso directo:** tratar el agua de producción (membranas de ósmosis inversa, evaporación térmica, oxidación avanzada) para reutilizarla en el siguiente pozo de fracturamiento, en vez de inyectarla como desecho.
- **Reúso de beneficio ambiental:** Texas ya está desarrollando permisos para reúso agrícola o vertimiento a ríos de agua tratada a estándares más altos — más caro, pero reduce el volumen total que necesita disposición profunda.
- **Meta realista para Colombia si autoriza fracking:** exigir por regulación, desde el primer contrato, una meta de reciclaje de agua de producción (ej. 50% desde el año 1, siguiendo el punto de partida real de Texas), no dejarlo como buena práctica voluntaria.

## 5. Propuesta: un gemelo digital de sismicidad inducida para Colombia

Colombia ya tiene la mitad de la infraestructura necesaria — no hay que construir desde cero:

**Lo que ya existe:**
- El **Servicio Geológico Colombiano (SGC)** opera la Red Sismológica Nacional de Colombia (RSNC), con monitoreo sísmico en tiempo real ya funcionando para sismos tectónicos.
- La ANM y la ANH ya exigen reportes operacionales de proyectos mineros y de hidrocarburos (volúmenes de extracción, y en el caso de fracking futuro, de inyección).

**Lo que falta construir (el gemelo digital propiamente dicho):**

1. **Capa de datos unificada:** integrar la telemetría operacional de cada proyecto (volumen inyectado o extraído, presión, profundidad) con los datos sísmicos de la RSNC del SGC en tiempo real — hoy son sistemas separados que no se cruzan automáticamente.
2. **Modelo de pronóstico con aprendizaje automático:** replicar la metodología ya documentada internacionalmente (modelos de pronóstico en tiempo real de sismicidad inducida, usados en almacenamiento geológico de CO2 y en pozos geotérmicos) para estimar la magnitud máxima esperable dado el ritmo de inyección/extracción actual — no es tecnología nueva, es tecnología ya validada en otros países que Colombia no ha adaptado todavía.
3. **Protocolo de semáforo con autoridad real de cierre:** a diferencia del caso de El Teniente (donde el supervisor de turno podía autorizar operación pese a sismicidad "fuera de rango"), el diseño institucional debe separar quién opera de quién tiene la autoridad de detener — recomendación: que el SGC (no el operador) tenga la potestad de activar el semáforo rojo, con obligación legal de acatamiento inmediato por parte de la ANM/ANH.
4. **Panel público de transparencia:** el mismo principio de `docs/03-estudios-colombia-y-ejecucion.md` — un tablero abierto donde comunidades vecinas a cualquier proyecto de minería subterránea profunda o fracking puedan ver el nivel de alerta sísmica vigente, no solo el operador y el regulador.

**Por qué esto es coherente con el resto de este repositorio:** ya se recomendó exigir InSAR y monitoreo de relaves como condición de licencia (`docs/06`); un gemelo digital de sismicidad inducida es la misma lógica aplicada a un riesgo distinto — medir en tiempo real en vez de auditar después del desastre.

**Fase realista de implementación:**
- **Meses 0-6:** convenio SGC-ANM-ANH para compartir datos operacionales en tiempo real (sin esto, no hay gemelo digital posible).
- **Meses 6-18:** piloto del modelo de pronóstico sobre un proyecto ya en operación con sismicidad conocida (candidato natural: cualquier mina subterránea profunda existente, para calibrar el modelo antes de que Quebradona entre en producción).
- **Meses 18-36:** protocolo de semáforo con autoridad legal real, exigible como condición de licencia para Quebradona y cualquier proyecto futuro de fracking.

## 6. La lección contractual de Groningen que Colombia no puede permitirse ignorar

Cuando Países Bajos decidió cerrar el campo de gas de Groningen por el riesgo sísmico a la población, **Shell y ExxonMobil demandaron al Estado holandés por miles de millones de dólares en tribunales de arbitraje privados (ISDS)** — usando exactamente el tipo de protección que los tratados de inversión les garantizan.

**Por qué esto le importa a Colombia antes de firmar cualquier contrato de fracking o de minería subterránea profunda:** si el país necesita cerrar o restringir un proyecto por riesgo sísmico ya en marcha (como El Teniente debió haber hecho el 31 de julio de 2025 y no hizo), y el contrato no anticipó esa posibilidad, el Estado colombiano queda expuesto al mismo tipo de demanda que hoy enfrenta el gobierno holandés. **Recomendación concreta:** cualquier contrato futuro de fracking o de minería subterránea profunda en Colombia debe incluir, desde la firma, una cláusula explícita de suspensión o cierre por riesgo sísmico verificado por el SGC, sin que eso constituya expropiación indirecta ni active cláusulas de protección de inversión — blindando jurídicamente al Estado antes de que la decisión de cerrar sea necesaria, no después.

---
*Ver también: [Análisis ampliado 2026-2050](01-analisis-ampliado-2026-2050.md) · [Soluciones jurídicas e institucionales](06-soluciones-juridicas-e-institucionales.md) · [IA, medición y fórmulas](02-ia-medicion-y-formulas.md)*
