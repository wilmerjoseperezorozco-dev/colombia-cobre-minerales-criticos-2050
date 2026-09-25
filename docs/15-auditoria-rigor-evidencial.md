# Auditoría de rigor evidencial: qué tan bien fundamentado está cada tema, y qué falta

> Ejercicio de revisión crítica, sin conflicto de interés en ninguna dirección: no busca inflar la credibilidad del repositorio ni desacreditarlo, busca ubicar con precisión dónde está parado cada bloque de la investigación en la escala primario/institucional → académico revisado por pares → prensa/secundario → estimación propia. Se hace explícitamente porque un repositorio que se auto-audita solo para confirmar que "todo está bien" no está siendo honesto con su propio método (ver `docs/09-metodologia-pipeline.md`, sección 1).

## 1. Metodología de esta auditoría (y su límite)

Se clasificaron los ~75 enlaces de `docs/05-fuentes.md` por dominio en 5 categorías, y se cruzó con una lectura temática de qué bloques de conclusiones del repositorio dependen de cada categoría. **Esto es una clasificación estructural por procedencia del dominio, no una verificación claim por claim** de cada afirmación — un artículo de Reuters puede ser periodismo riguroso citando una fuente primaria, y un paper académico puede estar mal hecho. Es un proxy útil para ver el *patrón* de dependencia evidencial, no un veredicto sobre la calidad de cada fuente individual.

## 2. Distribución actual de fuentes por categoría

| Categoría | Aprox. | Ejemplos | Lectura |
|---|---|---|---|
| **Primaria oficial / institucional** (gobierno, agencia internacional) | ~18 | UPME, USGS, IEA, SGC/CORTOLIMA, ANM, MinEnergía, ONU, FDSN | **Fortaleza real del repositorio.** La mayoría de las cifras centrales (potencial geológico, precio, demanda, reservas) vienen de aquí, con pipeline ejecutable que las re-verifica en cada corrida — no es un dato citado una vez y congelado. |
| **Académica / revisada por pares** | ~7 | ResearchGate (sismicidad Puerto Gaitán), MDPI ×2, ScienceDirect, Springer, revistas de la Universidad Nacional | **El eslabón más débil, en volumen.** Menos del 10% de las fuentes totales, y concentradas casi todas en un solo tema (IA aplicada a exploración/monitoreo) — casi ninguna sobre la geología del cobre colombiano en sí, la economía de la demanda, o la sociología de la minería ilegal. |
| **Prensa / medios (general y financiera)** | ~32 | Portafolio, El Tiempo, Infobae, Forbes Colombia, Mining.com, CNBC | **La categoría más grande, y la más volátil.** Necesaria para el componente de actualidad (el marco bilateral tiene 2 meses de firmado), pero es exactamente la categoría que ya produjo los 2 errores de integridad documentados en este repositorio (9,7→17,4 Mt; 34,5→27,8 Mtpa) — ambos originados en resúmenes de prensa sin verificar contra la fuente primaria citada. |
| **ONG / organismos de incidencia (advocacy)** | ~6 | Mongabay, MiningWatch Canada, SOMO, AIDA Américas, Colombia Check | Aportan la dimensión de impacto social/ambiental que ni gobierno ni prensa financiera suelen cubrir bien — pero tienen, por diseño institucional, una posición de partida crítica hacia la minería extractiva. No invalida sus datos, pero su marco interpretativo no es neutral y debe leerse como tal. |
| **Corporativa / relaciones con inversionistas** | ~7 | AngloGold Ashanti, ASML, Wood Mackenzie, S&P Global, US Funds | Útiles para cifras operativas puntuales, pero son fuentes con incentivo directo de presentar el sector de forma favorable a sus propios intereses (atraer capital, justificar valoración). Se usaron con esa cautela en este repositorio, pero vale dejarlo explícito. |

## 3. Lo que está sólidamente fundamentado (nivel primario, ejecutable, no solo citado)

- **Potencial geológico de Colombia** (17,4 Mt) — UPME primaria, verificada página por página, con la corrección documentada de un error propio de interpretación.
- **Precio del cobre** — FRED/FMI, en vivo, recalculado en cada corrida del pipeline (ver ADR_002 sobre por qué esta fuente).
- **Demanda y oferta global** — IEA Critical Minerals Data Explorer, dataset oficial (no un resumen de prensa), tras la corrección de la Fase 6.
- **Reservas y producción mundial** — USGS Mineral Commodity Summaries, parseado y testeado, con guardrail de plausibilidad.
- **Sismicidad inducida en Puerto Gaitán** — es, de hecho, el bloque temático con *mejor* respaldo académico de todo el repositorio: tiene un paper específico revisado por pares (no solo prensa) además de la fuente institucional del SGC.

## 4. Dónde el repositorio se apoya casi exclusivamente en prensa o síntesis secundaria (y qué buscar para cerrarlo)

Cruzando esto con los 8 ejes de búsqueda ya definidos en `docs/05-fuentes.md`:

| Tema del repositorio | Nivel actual de respaldo | Qué falta específicamente |
|---|---|---|
| **Geología del pórfido cuprífero colombiano en general** (más allá de las evaluaciones puntuales del USGS ya citadas) | Institucional (USGS/UPME), casi nada académico independiente reciente | Buscar literatura de economic geology post-2015 sobre el cinturón andino en Colombia específicamente — la referencia académica más citada en el propio informe de UPME (Sillitoe et al.) es de **1982**; verificar si hay reinterpretaciones geológicas más recientes que UPME no haya incorporado. |
| **Minería ilegal como economía criminal** (29/32 departamentos) | Institucional (UPME) + 1 fuente académica sobre agua en minería informal de oro (no cobre específicamente) | Casi no hay literatura académica sobre minería ilegal de **cobre** específicamente en Colombia (la literatura existente es abrumadoramente sobre oro) — es una laguna real de la literatura, no solo de este repositorio, y vale la pena decirlo así en vez de forzar una cita que no aplica. |
| **Modelos de demanda de cobre por transición energética/IA** | Institucional (IEA) + 0 papers académicos que auditen esos supuestos de forma independiente | Buscar literatura de economía energética que contraste los escenarios IEA con proyecciones académicas independientes — el propio IEA ha sido criticado en la literatura por historiales de proyección conservadores en energías renovables; no se ha verificado si ese sesgo aplica también a sus proyecciones de minerales críticos. |
| **Geopolítica de minerales críticos** (`docs/13`) | Prensa + análisis propio, 0 fuentes académicas de relaciones internacionales | Es el documento con la base evidencial más débil del repositorio en términos de literatura especializada — se apoya en el consenso divulgado por centros de análisis (CSIS/RAND/Chatham House) citado de memoria, no en publicaciones puntuales de esos centros con enlace verificable. Ver ADR_002 para el criterio ya aplicado a fuentes de precio; el mismo estándar debería aplicarse aquí. |
| **Gestión de relaves y estándar GISTM** | 2 fuentes de blogs especializados en tecnología (Geofem, Farmonaut), 0 académicas | Existe literatura académica real post-Brumadinho (2019) sobre falla de presas de relaves — no se ha incorporado ninguna a este repositorio todavía, pese a que `docs/06` y `docs/07` dependen de ese tema. |

## 5. Sesgos estructurales a vigilar activamente (no corregidos aquí, solo señalados)

1. **Sesgo de disponibilidad hacia lo reciente.** El repositorio está construido casi enteramente sobre eventos y datos de 2025-2026 — hay poca profundidad histórica más allá de la serie de precios (Fase 8) y ningún intento de contrastar el "boom" actual contra ciclos previos de interés minero en Colombia (hubo al menos un ciclo de interés fuerte en cobre/oro a mediados de la década de 2010 que colapsó con la caída de precios de commodities de 2014-2016 — no está documentado en este repositorio como precedente).
2. **Sesgo de fuente institucional favorable al sector.** UPME, ANM y Trade.gov (EE. UU.) tienen, por mandato, un rol de promoción del sector minero — no son fuentes neutrales sobre si la minería de cobre *debería* expandirse, aunque sí son fuentes confiables sobre las cifras técnicas que reportan. El repositorio ya compensa esto parcialmente con las fuentes de ONG/advocacy (categoría 4 de la tabla), pero el balance cuantitativo (18 institucionales vs. 6 de advocacy) sigue inclinado hacia el marco pro-desarrollo.
3. **Ausencia casi total de fuentes en el propio idioma técnico de las comunidades afectadas.** Las fuentes sobre impacto social (`docs/07`) son, en su mayoría, de ONG internacionales o prensa nacional — no hay literatura antropológica o etnográfica directamente sobre las comunidades de Chocó, Antioquia o Santander en las zonas de los proyectos ya identificados.

## 6. Recomendación priorizada (para la próxima ronda de búsqueda en `docs/05`)

Por impacto en la solidez del repositorio, en este orden:
1. Literatura académica sobre falla de presas de relaves post-Brumadinho (cierra la laguna más citada y con mayor riesgo humano de todo el repositorio).
2. Literatura de economic geology reciente sobre el cinturón cuprífero andino colombiano (la base geológica del proyecto depende hoy de una sola referencia de 1982).
3. Literatura académica (no de centros de análisis citados de memoria) sobre geopolítica de minerales críticos, para dar a `docs/13` el mismo nivel de rigor que el resto del repositorio.

---
*Ver también: [Fuentes consultadas y estrategia de búsqueda](05-fuentes.md) · [Metodología del pipeline](09-metodologia-pipeline.md) · [Hallazgos curiosos](14-hallazgos-curiosos.md)*
