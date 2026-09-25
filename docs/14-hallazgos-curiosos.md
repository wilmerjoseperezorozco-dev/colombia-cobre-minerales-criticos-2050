# Hallazgos curiosos: lo que más llama la atención de los datos ya reunidos

> Este documento es un artefacto vivo — se va a ir ampliando fase a fase, a medida que avancemos en el resto de la investigación (issues #8, #9, #14, #15, #16 y el monitoreo continuo). No repite los hallazgos principales ya cubiertos en `docs/01` o `docs/10` — recoge específicamente los datos que resultan sorprendentes, irónicos o contraintuitivos, con su fuente exacta dentro del repositorio.

## 1. El proyecto de cobre más avanzado del país es, hoy, 100% capital chino

El Alacrán (Córdoba) es el único proyecto de cobre colombiano con licencia ambiental completa — y su operador, JCHX Mining Management Co., cotiza en la Bolsa de Shanghái (603979.SS). El marco bilateral que Colombia firmó con Estados Unidos en Barranquilla busca explícitamente diversificar las cadenas de suministro de minerales críticos lejos de China. Es decir: el proyecto que mejor demuestra que Colombia sí puede producir cobre a escala es, en este momento, exactamente el tipo de exposición que el acuerdo busca reducir. *(`data/proyectos_cobre_colombia.json`, `docs/08-oportunidades-inversion.md`)*

## 2. Un "7" mal pegado hizo que Australia pareciera tener 71 veces más reservas de las reales

Al construir los tests de este pipeline se descubrió que la tabla mundial del USGS (Mineral Commodity Summaries) reportaba 7.100.000 kt de reservas de cobre para Australia, cuando la cifra real es 100.000 kt — un "7" de nota al pie del PDF que pdfplumber pegó al número durante la extracción de texto. El error llevaba tiempo sin detectarse, escondido detrás de un mensaje de éxito ("18/18 países parseados") que daba una falsa sensación de que todo estaba bien. *(`pipeline/phase5_usgs/fetch_usgs_copper_mcs.py`, función `_corregir_marcadores_de_nota_al_pie`)*

## 3. El cobre colombiano tiene una ley hasta 4,5 veces más alta que el promedio mundial

Los proyectos colombianos con estudios avanzados (El Roble, Quebradona) tienen tenores de cobre entre 1,2% y 3,6% — frente a un promedio mundial que ronda apenas el 0,8%. En minería, la ley del mineral determina directamente cuánta roca hay que mover (y cuánto relave generar) por cada tonelada de cobre producida: un yacimiento de mayor ley es, en igualdad de condiciones, más eficiente y menos invasivo por unidad de metal extraído. *(`data/upme_informe_cobre_hallazgos_curados.json`, sección de aspectos favorables, citando UPME)*

## 4. El pico de precio real más alto del cobre en 121 años no fue por autos eléctricos ni IA — fue la Primera Guerra Mundial

La serie histórica del USGS desde 1900 muestra que el valor unitario más alto de toda la serie en términos reales (dólares constantes de 1998) ocurrió en **1916** (USD 9.360/t), impulsado por la demanda bélica — un nivel que rivaliza con el súper-ciclo de China de 2011 y con el promedio de los últimos 5 años. El régimen de precios "sin precedentes" que vivimos hoy tiene, al menos, un antecedente real de hace más de un siglo. *(`docs/10-articulo-analisis-cientifico.md`, sección 3.8)*

## 5. Colombia ya tiene sismicidad inducida real desde 2013 — y no es por minería, es por agua

Puerto Gaitán (Meta) registró más de 900 sismos desde 2013, frente a solo 11 entre 1993 y 2013 — causados por la reinyección de hasta 4 millones de barriles diarios de agua de producción petrolera (el 95% de lo extraído). El SGC ya opera una red de monitoreo sísmico en tiempo real ahí, de forma aislada — es decir, la pieza técnica central de cualquier "gemelo digital" de sismicidad inducida para el país ya existe, funcionando, hace más de una década, solo que en un único sitio y sin generalizar. *(`docs/12-sismicidad-inducida-y-gemelo-digital.md`, sección 3.1)*

## 6. Un vacío regulatorio de una sola palabra dejó sin cobertura exactamente el mecanismo que causó los sismos de Puerto Gaitán

Cuando la comunidad de Puerto Gaitán pidió ante el Tribunal de Cundinamarca suspender las reinyecciones, el Ministerio de Minas alegó que su norma sobre sismicidad inducida "no aplicaba a campos convencionales" — la regulación existente solo cubría fracking (no convencional), dejando exactamente el tipo de operación (reinyección en campos convencionales) que causó el problema fuera de cualquier norma. *(`docs/12-sismicidad-inducida-y-gemelo-digital.md`, sección 3.1)*

## 7. El colapso que mató a 6 personas en Chile tuvo alertas 3,5 horas antes — y se ignoraron

En El Teniente (Chile), el 31 de julio de 2025, trabajadores en descanso reportaron explosiones "mucho más fuertes que las habituales" a las 14:00 horas. El colapso ocurrió a las 17:34. En el medio, la cadena de mando decidió no evacuar. Un procedimiento interno (P-03) permitía que un único supervisor de turno declarara la sismicidad "fuera de rango" y, en el mismo acto, autorizara que la operación continuara sin restricción — sin ningún mecanismo obligatorio de escalar la decisión a un especialista. Quebradona declara usar una técnica de explotación muy similar. *(`docs/12-sismicidad-inducida-y-gemelo-digital.md`, sección 2)*

## 8. La red sísmica de Colombia ya habla el mismo idioma técnico que el resto del mundo

Se verificó en vivo (no se asumió) que la Red Sismológica Nacional de Colombia está registrada en la Federación Internacional de Redes Sismográficas Digitales (FDSN), con DOI propio (`10.7914/SN/CM`), consultable por el mismo protocolo estándar que usan Chile, Japón o EE. UU. Una de sus estaciones activas (`CRJC`) está, literalmente, en Cerrejón, La Guajira — dentro de la misma zona de infraestructura pesada que este repositorio identificó como candidata para nueva industria. *(`docs/12-sismicidad-inducida-y-gemelo-digital.md`, sección 3.3)*

## 9. Un solo centro de datos de IA usa tanto cobre como entre 72.000 y 108.000 autos eléctricos juntos

Un vehículo eléctrico usa en promedio 83 kg de cobre. Un único centro de datos de IA de 300 MW requiere entre 6.000 y 9.000 toneladas — el equivalente al cobre de una ciudad entera de autos eléctricos, concentrado en un solo edificio. Y la demanda eléctrica de los centros de datos en EE. UU. va a pasar de representar ~5% del consumo eléctrico nacional en 2026 a un ~14% proyectado en 2030. Barranquilla, al mismo tiempo, se está posicionando como polo de centros de datos del Caribe — la misma ciudad puede terminar siendo puerto de salida del cobre y consumidora de la demanda que lo justifica. *(`data/consolidado/dataset_maestro.json → intensidad_de_cobre_por_uso`, `docs/04-estrategia-barranquilla.md`)*

## 10. El error de "9,7 Mt" que corregimos no era un error de digitación — era una mala lectura de un promedio regional

La cifra original (mal citada por este mismo repositorio antes de corregirse) mezclaba el potencial propio de Colombia con el promedio de tres regiones geológicas *compartidas* con Ecuador, Perú y Panamá (37,3 Mt). El potencial real y exclusivamente colombiano —17,4 Mt— resultó ser *mayor* que la cifra que se citaba como si fuera el total, no menor: la corrección fue hacia arriba, no hacia abajo. *(`docs/01-analisis-ampliado-2026-2050.md`, corrección del 14-sep-2026)*

## 11. La respuesta a una duda geológica de este repositorio llevaba 45 años publicada — solo que en Naciones Unidas, no en Colombia

Este mismo repositorio documentaba "El Infierno-Chili" como un prospecto de ubicación incierta, posiblemente en Huila o en la frontera con Ecuador. La respuesta real —Tolima, alojado en el Batolito de Ibagué— ya estaba en un informe técnico de Naciones Unidas de **1981**, redescubierto al triangularlo con una evaluación conjunta USGS-INGEOMINAS de 2008 y los límites del Páramo de Anaime-Chilí documentados por CORTOLIMA. De paso, se corrigió un error propio: este repositorio tenía el prospecto agrupado como parte del cinturón "Jurásico" cuando en realidad es Cretácico — una diferencia de más de 130 millones de años que nadie había cuestionado hasta cruzar la fuente primaria. *(`docs/11-geografia-sitios-candidatos.md`, sección 3, issue #15)*

---
*Ver también: [Análisis ampliado 2026-2050](01-analisis-ampliado-2026-2050.md) · [Metodología del pipeline](09-metodologia-pipeline.md) · [README / dashboard](../README.md)*
