# Análisis integrado de 3 objetivos de investigación: geocronología, geoquímica de plata y benchmarking metalúrgico

> Este documento aplica, con justificación teórica explícita, 5 fuentes académicas y técnicas (2 de Chile, 1 de Perú, y los datos primarios ya verificados de UPME/Atico Mining en este mismo repositorio) a 3 preguntas concretas sobre el cobre colombiano. Sigue la misma disciplina del resto del repositorio: cada inferencia distingue entre **dato verificado**, **hipótesis razonada** y **vacío de información real**, sin forzar conexiones entre sistemas geológicos que no las tienen (ver la corrección explícita en la sección 3.2).

## 1. Justificación

Tres brechas concretas, ya identificadas y documentadas en este repositorio, quedaron sin cerrar después de la auditoría de rigor evidencial (`docs/15`) y la primera ronda de literatura académica (`docs/05`, `docs/17`):

1. **Issue #18 (abierto):** la única referencia de edad geológica para el prospecto Infierno-Chili sigue siendo Sillitoe et al. **1982** — un solo método analítico, sin actualización en 44 años.
2. **Inconsistencia no resuelta en los datos de plata:** la Tabla 28 de UPME (`data/upme_informe_cobre_hallazgos_curados.json`) reporta plata como dato no disponible (`null`) para El Roble, mientras que sí reporta cifras para Quebradona (1.405.309 oz troy/año) y Soto Norte (2.950.000 oz troy/año) — sin que este repositorio hubiera verificado si esa ausencia es real o es un vacío de la fuente.
3. **Sin punto de comparación metalúrgico:** El Roble es la única mina de cobre en producción del país, pero hasta la sesión anterior este repositorio no tenía ningún dato de su eficiencia real de procesamiento (ley de concentrado, recuperación).

Este documento no busca confirmar una tesis previa — cada objetivo parte de una hipótesis nula explícita (sección 3) y se reporta el resultado la haya confirmado o no.

## 2. Marco teórico

### 2.1 Genética de depósitos de cobre y por qué el tipo de depósito importa

Un depósito de cobre no es una categoría única — el mecanismo de formación determina su geometría, su ley, sus elementos asociados y hasta su riesgo geotécnico. Los 3 tipos relevantes para este análisis, verificados contra fuente primaria (no supuestos):

| Tipo | Mecanismo | Ejemplo verificado en este análisis |
|---|---|---|
| Pórfido cuprífero | Intrusión magmática somera (~1-3 km), fluidos hidrotermales de alta temperatura circulando alrededor de un cuerpo ígneo | Quebradona, Soto Norte, El Alacrán, Infierno-Chili (Colombia) |
| Sulfuro masivo volcanogénico (VMS) | Precipitación de sulfuros en el fondo marino sobre o cerca de un sistema hidrotermal submarino ("black smoker"), posteriormente fosilizado por sedimentación/vulcanismo | **El Roble** (Chocó) — confirmado vía fuentes de la industria, no documentado antes en este repositorio |
| Estratoligado (*manto-type*) | Fluidos ascendiendo por fallas lístricas invertidas, precipitando el mineral al cruzar un frente redox en rocas favorables — sin relación directa con una intrusión centrada | Lo Aguirre (Chile) |
| Epitermal (análogo geotermal activo) | Fluidos hidrotermales someros (<1,5 km, <300°C) en sistemas volcánicos activos — el "análogo vivo" de yacimientos fósiles de Au-Ag de baja/intermedia sulfuración | Cerro Pabellón (Chile) |

**Por qué esto restringe qué comparaciones son válidas:** la práctica estándar en geología económica es comparar un depósito fósil contra su análogo moderno *del mismo mecanismo* — un VMS fósil se compara contra sistemas de *black smokers* submarinos activos, no contra un sistema geotermal subaéreo epitermal. Ignorar esta restricción fue, precisamente, el error que se corrigió en la conversación previa a este documento (ver sección 3.2).

### 2.2 Partición de elementos traza en calcopirita — por qué la plata es el trazador relevante aquí

La calcopirita (CuFeS₂) admite sustituciones acopladas de iones monovalentes (Cu⁺, Ag⁺), bivalentes (Zn²⁺, Cd²⁺, Pb²⁺), trivalentes (Fe³⁺, In³⁺, Sb³⁺) y tetravalentes (Se⁴⁺, Bi⁴⁺, Ge⁴⁺) — mecanismo descrito explícitamente en Reich et al. (2020) sobre Cerro Pabellón. La plata, en particular, entra en solución sólida junto con estas sustituciones y su concentración varía según la temperatura y la fuente magmática del fluido — en Cerro Pabellón, la razón Co/Ni baja se interpretó como indicio de una fuente magmática más félsica que en el sistema de referencia (Reykjanes, Islandia). **La teoría, entonces, predice que la plata en calcopirita no es un dato aislado — es un indicador del tipo de fuente magmática**, lo cual es exactamente lo que hace útil comparar sistemas epitermales/pórfido-epitermales entre sí (nunca un VMS contra un epitermal, ver 2.1).

### 2.3 Balance ley-recuperación en flotación — el marco para comparar plantas de distinta escala

En procesamiento de sulfuros de cobre por flotación, existe un compromiso estructural entre **ley del concentrado** y **recuperación metalúrgica**: maximizar la ley (concentrado más puro, menos costo de fundición) tiende a sacrificar recuperación (se pierde más cobre en la cola), y viceversa. Por eso comparar solo la ley del concentrado entre dos plantas sin considerar su recuperación simultánea puede llevar a una conclusión errónea sobre cuál es "más eficiente" — el criterio correcto es una comparación conjunta, no una sola cifra aislada.

## 3. Análisis por objetivo

### 3.1 Objetivo 1 — Geocronología: ¿la edad de 1982 para Infierno-Chili se sostiene?

**Hipótesis nula:** la edad Cretácica reportada por USGS (131 Ma, Batolito de Ibagué, citando Sillitoe et al. 1982) es consistente con lo que un método de datación multi-isotópico moderno encontraría.

**Método propuesto (transferido de Lo Aguirre, Saric et al. 2003):** isócrona Rb/Sr de roca total + K-Ar + ⁴⁰Ar/³⁹Ar sobre las mismas muestras, más δ³⁴S de sulfuros para inferir el origen del azufre.

**Lo que el caso de Lo Aguirre muestra que es posible, no lo que se espera encontrar en Colombia:** en Lo Aguirre, los 3 métodos radiométricos dieron edades escalonadas pero cercanas (113±3, 110±4, y 102±5 Ma) — una diferencia de 11 millones de años entre el método más antiguo (Rb/Sr, que data la cristalización inicial) y el más joven (⁴⁰Ar/³⁹Ar en albita, que data el cierre isotópico de una fase secundaria). El δ³⁴S (+0,5 a -3,6 ‰, cercano a cero) apuntó a azufre de origen magmático primario, y la razón ⁸⁷Sr/⁸⁶Sr inicial (0,7047) confirmó un componente magmático dominante con influencia de agua meteórica.

**Resultado de este análisis (no es un resultado de laboratorio, es la inferencia metodológica que justifica el paso siguiente):** si Infierno-Chili se dató una sola vez, con un solo método, en 1982 — la probabilidad de que ese único número capture correctamente tanto la edad de cristalización como cualquier evento hidrotermal secundario es baja, precisamente por lo que muestra el caso chileno: un solo depósito puede tener 11+ millones de años de diferencia entre eventos según qué mineral y qué sistema isotópico se date. **La hipótesis nula no puede confirmarse ni rechazarse con la información actual — solo se puede decir que es poco probable que una sola medición de 1982 sea la historia geocronológica completa.** Este es el resultado real: no "la edad está mal", sino "la incertidumbre alrededor de la edad es mayor de lo que el repositorio había asumido implícitamente al citar un solo número."

### 3.2 Objetivo 2 — Plata en calcopirita: Cerro Pabellón frente a Quebradona y Soto Norte (no El Roble)

**Corrección explícita antes de continuar:** una versión anterior de este análisis proponía comparar Cerro Pabellón (epitermal) contra El Roble. Se retractó al verificar que El Roble es un **VMS** — el análogo moderno correcto de un VMS es un *black smoker* submarino, no un sistema geotermal subaéreo. Esa comparación se elimina aquí, no se repite.

**Hipótesis nula:** los proyectos colombianos de tipo pórfido con componente epitermal (Quebradona, Soto Norte) no muestran nada que sugiera una fuente magmática comparable a la de Cerro Pabellón — la plata reportada en la Tabla 28 de UPME es simplemente un subproducto de la ley general del yacimiento, sin relación genética con el tipo de sistema magmático.

**Dato verificado (Tabla 28 UPME, ya en este repositorio antes de este análisis):**
- Quebradona: 1.405.309 oz troy de plata/año
- Soto Norte: 2.950.000 oz troy de plata/año — casi el doble por unidad de producción de cobre que Quebradona
- El Roble: `null` en esa misma tabla

**Hallazgo real de este análisis (verificado contra el Informe Técnico NI 43-101 de Atico Mining 2018, no un supuesto):** el `null` de El Roble en la Tabla 28 de UPME **es un vacío de la fuente, no un hecho geológico** — el informe técnico de Atico confirma que la plata en El Roble se ensaya de forma rutinaria (protocolo de control de calidad SGS específico para plata de alta ley), se paga en el contrato de venta de concentrado (US$0,35 por onza pagable, 95% del contenido) y tiene su propia tabla de análisis de sensibilidad de VAN. **No se pudo extraer una cifra exacta de onzas/año de plata de El Roble en esta pasada de revisión del PDF** (la Tabla 14.2 del informe menciona explícitamente estadísticas de plata pero la extracción de texto no capturó esas columnas) — se documenta como una corrección pendiente de completar, no se inventa el número.

**Sobre la hipótesis nula (Quebradona/Soto Norte vs. Cerro Pabellón):** no se pudo rechazar ni confirmar con los datos disponibles — se necesitaría el dato real de elementos traza en calcopirita de Quebradona/Soto Norte (que no existe públicamente, es exactamente el tipo de análisis que un piloto como el de `docs/17` generaría). Lo que sí se puede afirmar, calculando directamente desde los mismos datos de la Tabla 28 (Soto Norte: 4.680 t Cu/año, 2.950.000 oz Ag/año → 630,3 oz Ag por tonelada de Cu; Quebradona: 75.020 t Cu/año, 1.405.309 oz Ag/año → 18,7 oz Ag por tonelada de Cu), es que **Soto Norte es ~33,7 veces más rico en plata por tonelada de cobre que Quebradona** — una diferencia mucho mayor de lo que una lectura superficial de "ambos tienen plata" sugeriría, y un dato aritmético directo que este repositorio nunca había calculado explícitamente pese a tener ambas cifras desde hace semanas.

### 3.3 Objetivo 3 — Comparación metalúrgica real: El Roble frente a Pachacayo (Perú)

**Hipótesis nula:** El Roble opera en un rango de eficiencia metalúrgica comparable al reportado en la literatura para minas de escala similar; no hay una brecha real que justifique inversión adicional en optimización de planta.

**Datos verificados, ambos de fuente primaria:**

| Indicador | El Roble (NI 43-101, Atico Mining, prom. ene-2016 a jun-2018) | Pachacayo, Perú (tesis UNDAC, Guerra Vadillo 2019) |
|---|---|---|
| Ley de concentrado de Cu | 21,87% | 24% |
| Recuperación de Cu | 94,15% | No reportada en el resumen disponible |
| Recuperación de Au | 61,82% | No aplica (no es coproducto en Pachacayo) |
| Método | Trituración + molienda (80% pasante malla 200) + flotación, 4 bancos × 6 celdas, 850 tpd | Flotación experimental, muestreo aleatorio simple |
| Rango contractual exigido (El Roble) | 18-24% Cu | No aplica |

**Resultado real de este análisis:** El Roble opera dentro de su propio rango contractual (18-24% Cu) pero en la mitad baja, 2,13 puntos porcentuales por debajo de la ley de Pachacayo. **Esto no confirma la hipótesis nula de forma limpia, pero tampoco la rechaza con contundencia**, por la razón teórica de la sección 2.3: no se conoce la recuperación de Pachacayo, así que no se puede saber si esa mina logra mayor ley sacrificando recuperación (lo cual no sería, en neto, "más eficiente") o si de verdad supera a El Roble en ambos frentes. La comparación queda parcial, marcada como tal — no se completa con una conclusión que los datos no sostienen.

## 4. Discusión integrada

Los 3 análisis comparten un patrón: en ninguno de los 3 casos los datos disponibles permiten una conclusión cerrada — y eso, en sí mismo, es información útil. Cada uno señala con precisión qué dato exacto falta para cerrar la pregunta (edad multi-isotópica real de Infierno-Chili; cifra de plata de El Roble; recuperación de Pachacayo), en vez de rellenar el vacío con una estimación no verificada — exactamente la disciplina que el resto de este repositorio ya exige de sí mismo (ver `docs/15`, principio general).

Lo que sí queda establecido con certeza, no como hipótesis:
- El `null` de plata de El Roble en la Tabla 28 de UPME es un vacío de reporte, no un hecho geológico — hallazgo verificable y ya corregible.
- Soto Norte es ~33,7 veces más rico en plata por tonelada de cobre que Quebradona — dato aritmético directo de cifras que ya estaban en el repositorio, nunca antes calculado explícitamente.
- El Roble opera en la mitad baja de su propio rango contractual de ley de concentrado — un hecho operativo real, no una opinión.

## 5. Propuesta innovadora: Protocolo de Triple Huella para priorizar dónde explorar primero

Ninguno de los 3 objetivos, por separado, es una novedad metodológica — cada técnica (geocronología multi-isótopo, geoquímica de traza en calcopirita, benchmarking metalúrgico) es estándar en la industria. **Lo que no existe todavía —ni en este repositorio, ni, hasta donde se pudo verificar, en la literatura pública sobre el cinturón cuprífero colombiano— es un protocolo que combine las 3 dimensiones para decidir, con criterio explícito, en qué orden explorar el 97% del territorio sin caracterizar.**

**El protocolo, en 3 pasos, aplicado a un prospecto nuevo dentro de la Ronda ANM de 14 Áreas:**

1. **Huella geoquímica (barata, rápida — días):** análisis de elementos traza en calcopirita de muestras de superficie o testigos existentes, clasificado con el modelo de Li et al. ya integrado en `docs/17` — determina el tipo genético probable (pórfido, VMS, epitermal, estratoligado) sin necesitar datación.
2. **Huella de subproducto (barata, usa el mismo dato del paso 1):** si el perfil de elementos traza muestra plata elevada de forma consistente con fuente félsica (patrón Cerro Pabellón), el prospecto se marca como candidato a valor agregado por plata — relevante porque, como muestra el Objetivo 2, la diferencia de valor de plata entre proyectos ya conocidos (Soto Norte vs. Quebradona) es de ~33,7 veces por tonelada de cobre — una variable que hoy no se usa para priorizar exploración en Colombia.
3. **Huella de referencia metalúrgica (más cara, solo para los prospectos que pasan los 2 filtros anteriores):** pruebas de flotación a escala de laboratorio, comparadas contra los benchmarks reales ya establecidos en este documento (El Roble 21,87-24%, Pachacayo 24%) — para estimar, antes de invertir en una planta, si el concentrado probable cumple los rangos que exige un contrato de venta típico.

**Por qué esto es genuinamente nuevo, no una recombinación forzada:** cada paso usa un dato de bajo costo para decidir si vale la pena invertir en el siguiente, más caro — geocronología (el paso más caro de los tres, reservado solo para el Objetivo 1) nunca aparece en este protocolo de triaje inicial, precisamente porque el Objetivo 1 de este mismo documento mostró que su valor es resolver una duda genética profunda, no filtrar prospectos rápidamente. Es un uso deliberado y diferenciado de cada técnica según su costo y su pregunta, no la aplicación de las tres a todo por igual.

## 6. Limitaciones honestas de este documento

- Ninguna muestra colombiana fue analizada en este documento — todo el análisis es comparativo, sobre datos ya publicados de Colombia, Chile y Perú. Es un ejercicio de síntesis, no un nuevo dato de laboratorio.
- La cifra de plata de El Roble queda pendiente de extraer del informe técnico completo (Tabla 14.2) — no se inventó un número para completarla.
- La comparación metalúrgica del Objetivo 3 queda parcial por falta del dato de recuperación de Pachacayo.
- El Protocolo de Triple Huella (sección 5) es una propuesta de diseño, no un protocolo ya ejecutado ni validado contra un caso real colombiano.

---
*Ver también: [Diseño del piloto de prospectividad con IA](17-diseno-piloto-prospectividad-ia.md) · [Especificación técnica de monitoreo](16-especificacion-tecnica-monitoreo-relaves.md) · [Fuentes y estrategia de búsqueda](05-fuentes.md)*
