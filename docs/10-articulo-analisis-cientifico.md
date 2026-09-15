# Convergencia estratégica del cobre colombiano: análisis de un déficit estructural global frente a un potencial geológico subexplotado (2026–2050)

**Tipo de documento:** nota técnica de análisis estratégico, estructura IMRaD (Introducción, Métodos, Resultados, Discusión).
**Fecha de corte de datos:** 14 de septiembre de 2026 (curación) · última corrida del pipeline: ver `data/consolidado/dataset_maestro.json → generado_utc`.
**Reproducibilidad:** todos los cálculos de la sección de Resultados son reproducibles ejecutando `python pipeline/run_pipeline.py` (ver metodología completa en `09-metodologia-pipeline.md`).

## Resumen

Colombia posee un potencial geológico de cobre cuantificado por la Unidad de Planeación Minero-Energética (UPME), citando al USGS, en 17,4 millones de toneladas (Mt) distribuidas en dos regiones geológicas propias (7,7 Mt y 9,7 Mt), con un 97% del territorio nacional sin explorar. Simultáneamente, el mercado global de cobre presenta un régimen de precios alcista sostenido: la serie histórica oficial (FRED/FMI, 415 observaciones mensuales, 1992-2026) registra una tasa de crecimiento anual compuesta (CAGR) de 7,46% en los últimos 5 años, con un precio de cierre de la serie de USD 13.542,82 por tonelada (jul-2026). Este trabajo integra datos de mercado en vivo, literatura institucional colombiana e internacional, y un marco geopolítico recientemente formalizado (el marco Colombia–Estados Unidos de minerales críticos, sep-2026) para evaluar si Colombia está en posición de capturar esta ventana de precios altos, y qué variables institucionales —no geológicas— son las que determinan el resultado. Se encuentra que la variable dominante no es la disponibilidad de recurso ni el precio de mercado, sino la **estabilidad regulatoria y el origen de capital** de los proyectos ya en desarrollo, ejemplificado por el caso de El Alacrán (Córdoba), el proyecto más avanzado del país, hoy en manos de capital 100% chino.

## 1. Introducción

### 1.1 Planteamiento del problema

La transición energética global y la expansión de infraestructura de inteligencia artificial han generado un consenso de mercado sobre un déficit estructural de cobre hacia 2030-2035 (International Energy Agency [IEA], 2025; S&P Global, 2026). Colombia, con un potencial geológico documentado pero sin desarrollar (UPME, 2022, 2025), representa un caso de estudio de la brecha entre disponibilidad de recurso natural y capacidad institucional de capturarlo. Este trabajo pregunta: **¿qué variables explican que Colombia, con potencial geológico cuantificado, tenga hoy una sola mina de cobre a gran escala en producción?**

### 1.2 Hipótesis de trabajo

- **H1:** La restricción principal no es geológica sino regulatoria — la incertidumbre en el licenciamiento ambiental (ejemplo: Resolución 855/2025 sobre Quebradona) tiene mayor poder explicativo sobre el estancamiento del sector que la disponibilidad de recurso.
- **H2:** La ventana de precios altos y sostenidos (CAGR de 7,46% a 5 años, con precio actual >40% por encima del promedio de la ventana de 5 años) crea un incentivo de mercado suficiente para atraer capital externo, pero **no garantiza que ese capital provenga de los socios estratégicos declarados** (Estados Unidos), como lo demuestra el caso de El Alacrán.

## 2. Métodos

### 2.1 Fuentes de datos

| Fuente | Tipo | Método de obtención |
|---|---|---|
| FRED (Federal Reserve Bank of St. Louis), serie PCOPPUSDM | Serie de precios, origen FMI Primary Commodity Prices | Extracción automatizada vía API pública (`pipeline/phase2_live_fetch/`) |
| UPME — Mapa Metalogénico de Colombia; Caracterización socioambiental de proyectos de cobre (2025) | Datos geológicos y de proyectos | Revisión documental directa (citada en `docs/05-fuentes.md`) |
| Prensa especializada (El Colombiano, Portafolio, La República, Infobae) | Hechos verificables (fechas, montos de transacciones, licencias) | Revisión cruzada de al menos dos fuentes independientes por hecho reportado |
| IEA Global Critical Minerals Outlook 2025 | Escenarios de demanda (STEPS/APS/NZE) | Revisión documental |
| Jurisprudencia (Corte Constitucional, Consejo de Estado) | Marco legal | Revisión de sentencias citadas en fuentes secundarias especializadas (`docs/06-soluciones-juridicas-e-institucionales.md`) |

### 2.2 Procesamiento

La serie de precios se procesó con `pandas` (conversión de fechas, ordenamiento cronológico, cálculo de ventanas móviles de 1 y 5 años). El CAGR se calculó como:

```
CAGR = (Precio_final / Precio_inicial)^(1 / n_años) − 1
```

usando el primer y último valor de la ventana de 5 años más reciente disponible en la serie (61 observaciones mensuales). La volatilidad se calculó como la desviación estándar simple de la ventana correspondiente, sin ajuste estacional (limitación reconocida en la sección 5).

### 2.3 Criterios de inclusión de proyectos mineros

Se incluyeron los proyectos de cobre identificados independientemente por al menos dos fuentes (UPME 2025 y prensa especializada), listados en `data/proyectos_cobre_colombia.json`.

## 3. Resultados

### 3.1 Comportamiento del precio del cobre (dato en vivo, no estimado)

| Métrica | Valor | Ventana |
|---|---|---|
| Precio más reciente | USD 13.542,82/t | julio de 2026 |
| Promedio | USD 11.903,42/t | últimos 12 meses |
| Promedio | USD 9.608,58/t | últimos 5 años |
| Máximo histórico de la ventana | USD 13.552,04/t | últimos 5 años |
| Mínimo de la ventana | USD 7.544,81/t | últimos 5 años |
| CAGR | **7,46% anual** | últimos 5 años |
| Volatilidad (σ) | USD 1.517,10 | últimos 5 años |
| N observaciones | 415 (serie completa, 1992-2026); 61 (ventana de 5 años) | — |

**Lectura:** el precio actual (jul-2026) está apenas USD 9,22 por debajo del máximo de la ventana de 5 años, y 41% por encima del promedio de esa misma ventana — consistente con un régimen de mercado alcista sostenido, no un pico especulativo puntual (la volatilidad de 5 años y de 1 año son prácticamente idénticas: USD 1.517 vs. USD 1.510, lo que indica que el nivel de precios subió sin que aumentara proporcionalmente el ruido de corto plazo).

### 3.2 Estado de avance regulatorio vs. potencial geológico

De los 7 proyectos/rondas identificados en `data/proyectos_cobre_colombia.json`, solo **1 de 7** (El Roble) está en producción comercial; **1 de 7** (El Alacrán) tiene licencia ambiental completa pero capital 100% extranjero de un único país (China); **2 de 7** (Quebradona, Soto Norte) están frenados por trámites o superposición normativa; el resto está en exploración temprana o en fase de ronda de licitación. Es decir, el **85,7%** de los proyectos identificados no ha resuelto su situación regulatoria, pese a que el recurso geológico (17,4 Mt según UPME/USGS, ver sección 3.5) está documentado desde al menos 2019-2021.

### 3.3 Designación de mineral crítico en EE. UU. y su cronología frente al marco con Colombia

El USGS confirma (Mineral Commodity Summaries, edición de febrero de 2026, extraído directamente del PDF oficial) que el cobre fue incorporado a la Lista Final 2025 de Minerales Críticos de Estados Unidos el **7 de noviembre de 2025** (Federal Register 90 FR 50494), junto con plomo, potasa, renio, silicio y plata, tras un proceso de comentario público sobre una lista preliminar (90 FR 41591). Esta fecha es anterior en 10 meses al marco de cooperación firmado con Colombia en Barranquilla (8-sep-2026), lo que sitúa la secuencia causal en orden correcto: primero la designación doméstica de EE. UU. (nov-2025), después la búsqueda de socios de suministro externo (sep-2026) — un patrón consistente con la lógica declarada de "cadenas de suministro resilientes y diversificadas" del propio marco bilateral.

### 3.4 Reconciliación de cifras de oferta y demanda global (hallazgo metodológico, actualizado con fuente primaria IEA)

**Esta sección se revisó el 14-sep-2026** al incorporar el dataset oficial del IEA Critical Minerals Data Explorer 2026 (Fase 6 del pipeline, obtenido con cuenta gratuita del usuario — ver `pipeline/phase6_iea/`), que reemplaza una comparación anterior basada en una cifra de mercado no verificada contra fuente primaria.

| Fuente | Cifra 2025 | Qué mide exactamente |
|---|---|---|
| USGS MCS 2026 (oficial, gobierno de EE. UU.) | Producción de mina: 23.000 kt (2025e) · Producción de refinería: 27.955-29.000 kt (2025e) | Oferta física realizada, medida en el punto de producción |
| **IEA Critical Minerals Data Explorer 2026** (oficial, fuente primaria, Fase 6) | **Demanda total: 27.775 kt (2025, línea base)** | Consumo total modelado (energía + otros usos), metodología documentada y trazable |

**Corrección del hallazgo anterior:** con la fuente primaria de demanda (IEA, 27.775 kt) en vez de la cifra de mercado sin verificar que se usaba antes (34.500 kt, atribuida de forma imprecisa a "S&P Global/Wood Mackenzie" vía prensa), la oferta y la demanda de 2025 están **casi balanceadas** (27.775 kt de demanda vs. 27.955-29.000 kt de producción refinada) — **no hay evidencia de un déficit ya observable en 2025** como se afirmaba en una versión previa de este documento. Esa afirmación se retracta explícitamente.

**Dónde sí aparece un déficit real y bien fundamentado:** el propio dataset de IEA, comparando su demanda (escenario Stated Policies) contra su oferta "base case" (solo minas existentes y en construcción, sin proyectos nuevos) en los **mismos años y con la misma metodología**, muestra una brecha que crece de 6.799 kt (2030) a 17.801 kt (2040) — casi se triplica en una década (cálculo propio reproducible, ver `data/metricas_demanda_global_cobre.json` → `brecha_oferta_demanda_calculada_kt`). Esta es la evidencia que **sí sostiene H2** de forma robusta: el déficit es real, pero es una proyección de mediano plazo bien fundamentada, no un fenómeno ya presente en 2025.

### 3.5 Escala del potencial colombiano frente a las reservas mundiales oficiales

**Nota de corrección metodológica (14-sep-2026):** la fuente primaria de UPME (Informe Cobre, Tabla 1, verificada directamente en la Fase 7 del pipeline, ver `docs/09-metodologia-pipeline.md`) establece que Colombia tiene **dos regiones geológicas propias** con recursos hipotéticos de 7,7 Mt y 9,7 Mt (total **17,4 Mt**); la cifra de 37,3 Mt citada en versiones previas de este análisis es, según el propio texto de UPME, el *promedio* de otras tres regiones **compartidas** con Ecuador, Perú y Panamá — no un total exclusivo de Colombia. Esta sección usa la cifra corregida (17,4 Mt).

Usando la cifra de reservas mundiales del USGS (980.000 kt = 980 Mt) como denominador, el potencial de Colombia (17,4 Mt) representa el **1,78% de las reservas mundiales conocidas** (antes de la corrección se había calculado erróneamente 0,99%). Colombia no aparece como línea individual en la tabla de USGS — queda agregada dentro de "Other countries" (210.000 kt de reservas), bolsa sobre la cual el potencial colombiano representaría el **8,29%** (antes 4,62%). Este dato contextualiza con precisión las afirmaciones de prensa sobre Colombia como "potencia mundial del cobre" (ver `docs/05-fuentes.md`): el potencial es real y algo mayor de lo que se había calculado en la primera pasada de este análisis, pero su escala relativa frente a Chile (180.000 kt de reservas, 18,4% del total mundial) o Perú (85.000 kt, 8,7%) sigue siendo modesta — Colombia compite por ser un proveedor relevante de nicho dentro de la diversificación de EE. UU., no por desplazar a los líderes regionales establecidos.

**Nota sobre integridad del proceso:** esta corrección es en sí misma un resultado relevante del método: la cifra errónea ("9,7 Mt de un total de 37,3 Mt") se había originado en una lectura apresurada de un resumen periodístico y se propagó sin cuestionarse por varias secciones de este mismo repositorio hasta que la Fase 7 del pipeline forzó la verificación directa contra el texto original de la fuente primaria. Se documenta el error y la corrección en vez de silenciarlos, consistente con el estándar de reproducibilidad declarado en la cabecera de este documento.

### 3.6 Concentración de origen de capital

De los proyectos con operador identificado, la distribución de origen de capital es: Canadá (3 de 6: Atico Mining, Aris Mining, GoldMining/Cordoba histórico), China (1 de 6: JCHX vía El Alacrán), Sudáfrica (1 de 6: AngloGold Ashanti), y capital mixto Canadá/Medio Oriente (1 de 6: Soto Norte). **El proyecto con mayor avance regulatorio (licencia ambiental completa) es, específicamente, el de origen chino** — una correlación negativa entre "alineación geopolítica declarada por Colombia" (el marco con EE. UU.) y "avance regulatorio real observado", que soporta H2.

### 3.7 Recursos, reservas e impacto económico por proyecto (fuente primaria UPME)

La Fase 7 del pipeline extrajo y parseó automáticamente las tablas de recursos/reservas (estándares NI 43-101, JORC y SAMREC, según el proyecto) de los 5 proyectos cupríferos con estudios técnicos internacionales, directamente del informe técnico de UPME (ver `data/live/upme_recursos_reservas_proyectos.json`):

| Proyecto | Recursos totales aprox. | Ley de Cu | Reservas (si existen) |
|---|---|---|---|
| El Roble | 1,17 Mt medidos+indicados | 4,30% Cu | — (mina en producción, sin reserva NI 43-101 reportada en la fuente) |
| Quebradona | 599 Mt (indicados+inferidos) | 0,64% Cu promedio | 109,7 Mt probables @ 1,21% Cu |
| Soto Norte | 68,8 Mt (indicados+inferidos) | 0,17-0,19% Cu (depósito de Au con Cu subproducto) | 28,5 Mt probables @ 0,14% Cu |
| Mocoa Cu-Mo | 636 Mt inferidos | 0,33% Cu, 0,036% Mo | — |
| San Matías (incl. El Alacrán) | 98,3 Mt (indicados+inferidos) | 0,51% Cu (indicados) | — |

Dos hallazgos adicionales de esta tabla: (1) los depósitos colombianos con mayor ley de cobre (El Roble, Quebradona: 1,2%-4,3% Cu) están **por encima** del promedio de los grandes productores mundiales (mayoría ~0,8% Cu según UPME, citando USGS 2014) — una ventaja comparativa real; y (2) el propio análisis oficial de UPME concluye que ni siquiera Quebradona, el proyecto colombiano con más recursos, alcanza el 50% de las reservas de los principales proyectos en operación en el mundo — consistente con la sección 3.5.

El informe de UPME (Tabla 28, transcrita a mano en `data/upme_informe_cobre_hallazgos_curados.json` por tener encabezados de columna rotados no auto-parseables) estima que la inversión combinada de **Quebradona + Soto Norte asciende a ~USD 8.500 millones**, con ~1.550 empleos directos anuales combinados, USD 61,5 millones/año en regalías y USD 284,1 millones/año en impuesto de renta — una cifra oficial que valida, en el orden de magnitud correcto, la estimación propia razonada de USD 5.000-8.000 millones que el informe original de este repositorio había calculado de forma independiente antes de acceder a esta fuente primaria.

### 3.8 Perspectiva histórica: ¿es este realmente un régimen de precios sin precedentes? (Fase 8, USGS DS140)

La serie histórica de EE. UU. desde 1900 (USGS Data Series 140, 121 años) permite contrastar el régimen de precios actual (sección 3.1) contra más de un siglo de datos, no solo contra los últimos 5 años. Hallazgo notable: el **valor unitario más alto de toda la serie en términos reales (dólares constantes de 1998) ocurrió en 1916** (USD 9.360/t), impulsado por la demanda de la Primera Guerra Mundial — un nivel que **rivaliza con el pico nominal de 2011** (USD 8.950/t, el súper-ciclo de China) y con el promedio de los últimos 5 años de la serie FRED (USD 9.608/t, sección 3.1).

**Advertencia de comparabilidad:** la serie de FRED está en dólares nominales corrientes, mientras que la cifra de USGS de 1916 está deflactada a dólares de 1998 — no son directamente comparables sin una serie de deflactor de precios (IPC) que convierta ambas a una base común, ejercicio que queda fuera del alcance de este documento y se señala explícitamente como limitación (ver sección 5). Lo que sí es válido afirmar sin ese ajuste: **el mercado del cobre ha atravesado al menos un episodio de precios reales tan altos como el actual hace más de un siglo**, impulsado por una demanda excepcional (guerra) en vez de por transición energética — un recordatorio de que los "regímenes de precios sin precedentes" en cobre no lo son tanto si se mide con suficiente perspectiva histórica, aunque los motores estructurales de esta vez (electrificación + IA, sección 3.4) son de naturaleza más duradera que un conflicto bélico puntual.

## 4. Discusión

Los resultados son consistentes con H1: el diferencial entre potencial geológico (documentado, estable, conocido desde hace años) y desarrollo real (1 mina en producción) es demasiado grande para explicarse por falta de recurso; la variable que varía y explica la dispersión de resultados entre proyectos es el estado regulatorio (licencia obtenida vs. bloqueada vs. en trámite).

Respecto a H2, el hallazgo es más matizado de lo esperado: el mercado sí respondió al régimen de precios altos (evidenciado por la inversión de capital extranjero en múltiples proyectos), pero el capital que efectivamente llegó a la etapa más avanzada (licencia ambiental completa) no proviene del socio estratégico que Colombia formalizó apenas días antes en el mismo territorio donde se firmó el acuerdo (Barranquilla). Esto sugiere que **la señal de precio y la señal geopolítica operan en relojes distintos**: el capital privado se mueve más rápido que la diplomacia de Estado, y ya ocupó la posición de mayor valor (el proyecto con licencia) antes de que el marco bilateral pudiera influir en la decisión.

## 5. Limitaciones

1. La serie de precios (FRED/FMI) es un promedio de mercado global, no un precio de referencia específico para el cobre colombiano (que no cotiza de forma diferenciada por no tener producción a escala relevante todavía).
2. El cálculo de CAGR usa un punto inicial y un punto final de la ventana; es sensible a la elección exacta de esos dos puntos y no captura la trayectoria completa (una limitación reconocida de esta métrica, no específica de este análisis).
3. La clasificación de "origen de capital" en la sección 3.6 usa la nacionalidad de incorporación de la empresa operadora, que no siempre coincide con el origen último del capital accionario (ej. fondos de inversión con múltiples jurisdicciones).
4. Los datos de UPME (potencial geológico) tienen como base metodológica el Mapa Metalogénico de 2020-2022; no se identificó una actualización posterior en las fuentes consultadas, lo cual es en sí mismo un hallazgo relevante (ver `docs/03-estudios-colombia-y-ejecucion.md`, sección de brechas).
5. La Fase 3 del pipeline (snapshots de fuentes oficiales) es un sensor de cambios, no una fuente de datos cuantitativos — no se usó para ningún cálculo de esta sección.
6. La cifra de inversión de El Roble en la Tabla 28 de UPME (USD 9.475 millones) es inconsistente con su escala real de producción (~40.000 t/año de concentrado) frente a Quebradona y Soto Norte — probablemente refleja inversión acumulada histórica y no capex comparable; se reporta tal cual aparece en la fuente y se marca como no verificada, sin corregirla unilateralmente (ver `data/upme_informe_cobre_hallazgos_curados.json`).
7. Este documento fue corregido el 14-sep-2026 tras detectar un error propio de interpretación sobre el potencial geológico de Colombia (ver sección 3.5); no puede descartarse que existan otros errores de interpretación aún no detectados en secciones que dependen de fuentes secundarias de prensa en lugar de documentos primarios.
8. La sección 3.4 fue corregida el mismo día tras incorporar el dataset oficial de IEA (Fase 6): la afirmación anterior de un "déficit ya observable en 2025" se basaba en una cifra de demanda de prensa no verificada y se retracta explícitamente — el patrón se repite con el hallazgo de la sección 3.5, lo que sugiere una regla general de trabajo hacia adelante: **toda cifra citada solo de un resumen periodístico debe tratarse como provisional hasta verificarse contra la fuente primaria**.
9. La comparación histórica de la sección 3.8 mezcla una serie en dólares nominales (FRED) con una serie deflactada a dólares de 1998 (USGS DS140) sin una conversión formal entre ambas bases — la lectura cualitativa (que 1916 rivaliza con los picos modernos) es razonable, pero cualquier cifra exacta de "cuánto más alto" un período fue respecto al otro requeriría una serie de deflactor de precios (IPC de EE. UU.) que este análisis no incorporó.

## 6. Conclusiones

1. El recurso geológico no es la variable limitante del desarrollo cuprífero colombiano; la variable limitante es la estabilidad regulatoria.
2. El régimen de precios (CAGR 7,46% a 5 años, precio actual cerca del máximo de la ventana) es favorable y está documentado con datos oficiales en vivo, no solo con proyecciones.
3. Existe una desalineación observable entre la estrategia geopolítica declarada (diversificar lejos de China) y el resultado de mercado observado (el proyecto más avanzado es de capital chino) — esta desalineación es el hallazgo más citable de este análisis y debería ser el punto de partida de cualquier política pública que se diseñe a partir de este documento.
4. El potencial geológico específico de Colombia es 17,4 Mt (no 9,7 Mt), y aun así representa apenas 1,78% de las reservas mundiales — el discurso de "potencia mundial del cobre" debe matizarse: Colombia tiene una ventaja real en ley de mineral (1,2%-4,3% Cu frente al ~0,8% mundial) pero una desventaja real en volumen frente a Chile y Perú.
5. La cifra oficial de UPME de ~USD 8.500 millones de inversión combinada para solo 2 de los 5 proyectos analizados confirma que el orden de magnitud de inversión sectorial de la década (sección 9 del informe original) es razonable, y probablemente conservador si se cuentan los 3 proyectos restantes y la ronda de 14 áreas.

## Referencias

Ver listado completo con enlaces en [`docs/05-fuentes.md`](05-fuentes.md). Fuentes de datos primarios usadas directamente en los cálculos de la sección 3: Federal Reserve Bank of St. Louis (FRED), serie PCOPPUSDM; Unidad de Planeación Minero-Energética (UPME), 2022 y 2025; International Energy Agency (IEA), *Global Critical Minerals Outlook 2025*; prensa especializada citada por hecho específico en `data/proyectos_cobre_colombia.json`.

---
*Ver también: [Metodología del pipeline](09-metodologia-pipeline.md) · [Análisis ampliado 2026-2050](01-analisis-ampliado-2026-2050.md) · [Soluciones jurídicas e institucionales](06-soluciones-juridicas-e-institucionales.md)*
