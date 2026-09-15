# Metodología del pipeline de datos

## 1. Filosofía: investigar primero, automatizar después

El orden de construcción de este repositorio fue deliberado: primero la investigación humana curada (sesiones 1-2, con verificación cruzada de fuentes), y solo después la automatización. Automatizar sin haber investigado primero produce pipelines que extraen datos sin criterio para interpretarlos; investigar sin después automatizar produce un informe estático que se desactualiza en semanas. Este pipeline es el punto donde ambos se encuentran.

## 2. Arquitectura por fases

```
pipeline/
├── phase1_seed/               Valida el dataset curado a mano (bloqueante)
├── phase2_live_fetch/         Extrae datos en vivo de APIs públicas reales (bloqueante)
├── phase3_scrape_oficiales/   Snapshot de páginas oficiales colombianas sin API (no bloqueante)
├── phase5_usgs/                Extrae y parsea el PDF oficial del USGS (Copper) (no bloqueante)
├── phase6_iea/                 Ingesta manual del Excel oficial de IEA (no bloqueante)
├── phase7_upme_sgc/            Extrae y parsea el informe técnico UPME de cobre (no bloqueante)
├── phase8_usgs_historia/       Serie histórica de EE.UU. desde 1900, USGS DS140 (no bloqueante)
├── phase4_consolidacion/      Une todo en un dataset maestro con procedencia (bloqueante, corre último)
├── schema/                    Esquemas JSON de validación
├── _manual_uploads/            Archivos aportados por el usuario (ej. el Excel de IEA) que la Fase 6 consume
└── run_pipeline.py            Orquestador — corre las fases en orden (1→2→3→5→6→7→8→4)
```

| Fase | Qué hace | Tipo de fuente | Bloqueante |
|---|---|---|---|
| 1 — Semilla | Valida `data/*.json` curados por investigación humana contra un esquema | Investigación manual verificada | Sí |
| 2 — Extracción en vivo | Descarga la serie histórica de precio del cobre desde FRED (API pública, sin key) | API pública real | Sí |
| 3 — Snapshot oficial | Descarga el HTML de ANM/UPME/SGC/ANLA y detecta cambios por hash | Páginas oficiales sin API | No (best-effort) |
| 5 — USGS MCS (Copper) | Descarga y parsea con `pdfplumber` la ficha oficial de cobre del USGS: estadísticas de EE. UU., producción/reservas mundiales por país, designación de mineral crítico | PDF oficial con formato tabular estable | No (best-effort — depende de que el USGS no cambie el diseño del PDF) |
| 6 — IEA Critical Minerals | Ingesta el Excel oficial de IEA (demanda por escenario + oferta minera "base case") aportado por el usuario desde su cuenta gratuita — IEA no ofrece API pública para esto | Excel oficial, sin API disponible (confirmado) | No (se omite si el archivo no está presente) |
| 7 — UPME Informe Cobre | Descarga y parsea con `pdfplumber` el informe técnico de UPME: potencial nacional (Tabla 1) y recursos/reservas de los 5 proyectos (Tablas 2-8) | PDF oficial, formato tabular con particularidades de extracción (ver 2.3) | No (best-effort) |
| 8 — USGS DS140 (histórico) | Resuelve dinámicamente la URL del Excel vigente en la página de USGS y descarga la serie de EE. UU. 1900-2020 (producción, consumo, precio nominal y real, producción mundial) | Excel oficial, URL resuelta en tiempo de ejecución (no hardcodeada) | No (best-effort) |
| 4 — Consolidación | Une todo lo anterior en `data/consolidado/dataset_maestro.json`, marcando el origen y confiabilidad de cada bloque, y calcula métricas derivadas (CAGR, volatilidad) | — | Sí |

### 2.1 Fase 5 en detalle — por qué un PDF sí se puede parsear de forma confiable aquí

A diferencia de las páginas HTML de la Fase 3 (sin estructura consistente), el Mineral Commodity Summaries del USGS es una publicación anual con un **formato tabular que se ha mantenido estable durante años** y un patrón de URL predecible (`mcs{año}-copper.pdf`). Eso lo hace parseable con reglas, con dos salvaguardas explícitas en el código:

- Cada país esperado en la tabla mundial se busca por nombre exacto; si no aparece (porque el USGS cambió el formato), se reporta como advertencia explícita en vez de fallar en silencio o inventar un valor.
- Los párrafos de texto libre (como la designación de mineral crítico) se parsean sobre una versión del texto con saltos de línea normalizados, porque pdfplumber conserva los cortes de línea del PDF a mitad de oración — un error real que apareció durante la construcción de este script y quedó corregido (ver commit correspondiente).

**Hallazgo más importante que produjo esta fase:** el cobre fue añadido a la Lista Final 2025 de Minerales Críticos de EE. UU. el **7 de noviembre de 2025** (Federal Register 90 FR 50494) — un dato que no estaba en ninguna otra fuente ya integrada al pipeline y que explica, con fecha exacta, por qué el marco de cooperación con Colombia se firmó apenas 10 meses después.

### 2.2 Fase 6 en detalle — cuando la fuente oficial no tiene API (y el usuario aporta el archivo)

`pipeline/phase6_iea/ingest_iea_manual.py` ingesta el archivo Excel oficial "IEA Critical Minerals Dataset 2026", descargado por el usuario con su cuenta gratuita de IEA. Se verificó explícitamente que IEA **no ofrece una API pública ni una clave programática** para este dataset a través de una cuenta gratuita: el botón de descarga en el Critical Minerals Data Explorer exige una sesión de navegador autenticada (usuario/contraseña), confirmado navegando la página con el Browser pane — apareció un formulario de login, no un token. Automatizar esa descarga requeriría manejar credenciales, algo que este pipeline no hace por política.

**Patrón de "ingesta manual honesta":** el archivo se coloca en `pipeline/_manual_uploads/`, la fase lo lee de ahí, y **se omite sin fallar** (`return 0`) si el archivo no está presente — no es bloqueante porque depende de una acción humana externa al pipeline, igual en espíritu a la Fase 3 (que tampoco pretende ser una API donde no la hay).

**Qué se ganó con esta fuente:** el dataset oficial de IEA permitió reemplazar cifras de demanda global que este repositorio citaba de un resumen de prensa (34,5/42/70+ Mtpa, atribuidas de forma imprecisa a "S&P Global/Wood Mackenzie") con la cifra primaria real (27.775 kt en 2025, hasta 38.066 kt en 2050 bajo el escenario más agresivo del propio IEA) — un segundo caso, además del de la sección 2.1/UPME, donde verificar contra la fuente primaria cambió una conclusión ya publicada en este repositorio (ver `docs/10-articulo-analisis-cientifico.md`, sección 3.4).

**Aviso de licencia:** el archivo se conserva en el repositorio (privado) para reproducibilidad, con un aviso explícito en el JSON de salida de que es para uso personal/no comercial de la cuenta gratuita del usuario — no debe redistribuirse el Excel crudo si este repositorio deja de ser privado.

**Flujo manual exacto (para quien retome este proyecto en 6 meses, incluyéndome a mí):**

1. Crear una cuenta gratuita en [iea.org](https://www.iea.org/) si no se tiene una (Join for free).
2. Ir a [Critical Minerals Data Explorer](https://www.iea.org/data-and-statistics/data-tools/critical-minerals-data-explorer).
3. Iniciar sesión (el botón de descarga redirige a un formulario de login — confirmado, no es un token).
4. Buscar el enlace/botón **"Download supply & demand data behind the Critical Minerals Data Explorer 2026 edition"** y descargarlo (Excel, ~1,1 MB).
5. Guardar el archivo como `pipeline/_manual_uploads/IEA_Critical_Minerals_Dataset_2026.xlsx` (ese nombre exacto — es lo que `ingest_iea_manual.py` busca).
6. Correr `python pipeline/phase6_iea/ingest_iea_manual.py` (o el pipeline completo).

**Cómo saber si es el archivo correcto (verificación de hash):** el archivo usado para todos los análisis de este repositorio tiene el siguiente hash SHA-256:

```
43bd9338a08ac8399c65471115f30ffc10dca7117e62f03cca86d49224717935
```

Verificar con `python -c "import hashlib; print(hashlib.sha256(open('pipeline/_manual_uploads/IEA_Critical_Minerals_Dataset_2026.xlsx','rb').read()).hexdigest())"`. Si el hash difiere, **no es necesariamente un error** — puede ser simplemente que IEA actualizó el dataset con datos más recientes; en ese caso, correr la Fase 6 y revisar si los números de `docs/01`/`docs/10` cambiaron significativamente antes de dar por buena la actualización.

### 2.3 Fase 7 en detalle — el informe técnico UPME y una lección de infraestructura de datos

`pipeline/phase7_upme_sgc/fetch_upme_informe_cobre.py` descarga y parsea el informe técnico "Informe Cobre" de la Subdirección de Minería de UPME (~95 páginas), la fuente con más tablas de recursos/reservas (NI 43-101/JORC/SAMREC) de todo el corpus consultado.

**Hallazgo de infraestructura verificado con DNS-over-HTTPS:** la URL que cita el propio documento en su bibliografía (`www1.upme.gov.co/...`) **no resuelve en DNS público** (`Status: NXDOMAIN` consultado directamente contra `dns.google`, no solo un fallo de este entorno). El dominio operativo real migró a `docs.upme.gov.co` (sitio reconstruido en WordPress). Este script usa la URL que efectivamente responde HTTP 200, documentando la discrepancia — un ejemplo concreto, no anecdótico, de la brecha de acceso a datos oficiales colombianos que `docs/03-estudios-colombia-y-ejecucion.md` ya señalaba de forma general.

**Corrección metodológica que produjo esta fase:** al verificar contra el texto original la cifra "9,7 Mt de un cinturón de 37,3 Mt" que este repositorio había repetido desde la sesión anterior, se encontró que la interpretación era incorrecta — ver el detalle completo en `docs/10-articulo-analisis-cientifico.md`, sección 3.5. El potencial correcto de Colombia es **17,4 Mt** (dos regiones geológicas propias). Esto se corrigió en `data/potencial_colombia_y_retos.json`, `data/estudios_cientificos_colombia.json`, `data/kpis_hoja_de_ruta_2026_2050.json` y en los documentos `01`, `03` y `10`.

**Qué se automatizó vs. qué se transcribió a mano:** las tablas de recursos/reservas por proyecto (Tablas 1-8 del documento) tienen texto lineal parseable con expresiones regulares, aunque con un reto real — pdfplumber extrae las etiquetas de categoría (ej. "Recursos Medidos") partidas alrededor de la fila numérica en vez de antes de ella, por el ajuste de línea de la celda PDF original; el script maneja esto explícitamente. La Tabla 28 (comparativo económico) tiene encabezados rotados 90° que pdfplumber invierte carácter por carácter — ahí se optó por transcripción manual con cita de página exacta, en `data/upme_informe_cobre_hallazgos_curados.json`, en vez de forzar un parseo frágil.

### 2.4 Fase 8 en detalle — resolver la URL en tiempo de ejecución, no hardcodearla

`pipeline/phase8_usgs_historia/fetch_usgs_ds140_copper.py` descarga la serie histórica de cobre de EE. UU. desde 1900 (USGS Data Series 140). A diferencia de la Fase 5 (URL con patrón predecible `mcs{año}-copper.pdf`), el archivo real de esta fase vive en un bucket S3 con nombre versionado (`ds140-copper-2020.xlsx`) enlazado desde una página HTML de aterrizaje — si USGS publica una actualización, el nombre del archivo cambiará (ej. a `ds140-copper-2023.xlsx`). Por eso el script **no hardcodea el nombre del archivo**: descarga primero la página HTML y extrae con una expresión regular el enlace `.xlsx` vigente, luego descarga ese archivo. Esto es más robusto que la Fase 5 frente a actualizaciones de la fuente, al costo de una dependencia adicional (que la página HTML mantenga el mismo patrón de enlace).

**Qué complementa:** la Fase 2 (FRED) cubre precio mensual 1992-2026; esta fase aporta 92 años adicionales (1900-2020) de producción primaria/secundaria de EE. UU., comercio exterior, consumo, valor unitario nominal y ajustado por inflación (dólares de 1998), y producción mundial — con esto, cualquier afirmación sobre "precios históricamente altos" en `docs/10-articulo-analisis-cientifico.md` puede contrastarse contra más de un siglo de datos, no solo contra los últimos 33 años.

### 2.5 Fase 9 en detalle — auditoría por catálogo, no extracción total (402 páginas)

`pipeline/phase9_upme_auditoria/audit_upme_docs_adicionales.py` procesa los 2 documentos de UPME que la Fase 7 dejó pendientes: "Documento_Cobre_29-12-2023.pdf" (240 págs.) y "Definitivo_Caracterizacion...2025.pdf" (162 págs.) — 402 páginas combinadas. Extraer cada tabla de ambos con el mismo nivel de detalle que la Fase 7 no habría sido proporcional: una inspección preliminar confirmó que son mayormente análisis social/demográfico por municipio (población, pobreza, salud, educación), no fichas técnicas de recursos minerales.

**Qué hace en su lugar:** cataloga **todas** las tablas de ambos documentos (número, página, título) con expresiones regulares sobre `Tabla N.`, y las clasifica por palabras clave en 4 categorías (`ambiental`, `demografico_social`, `economico_financiero`, `recursos_reservas`). Dos bugs reales aparecieron y se corrigieron durante la construcción: (1) el clasificador inicial confundía "recurso hídrico" con recurso mineral por buscar la palabra genérica "recurso" — se resolvió dando prioridad de verificación a la categoría ambiental antes que a la de recursos minerales, y usando frases más específicas ("recursos minerales", "recursos y reservas") en vez de la palabra suelta; (2) la "Lista de tablas" (índice) de cada documento generaba entradas duplicadas con líderes de puntos y número de página al final del título (ej. "...Chocó ........... 47") — se filtran con una expresión regular que detecta ese patrón.

**Resultado del catálogo (165-168 tablas por documento, tras deduplicar):** cero tablas de la categoría `recursos_reservas` en ninguno de los dos documentos — confirma que no hay cifras de recursos/reservas minerales sin capturar todavía. Sí aparecieron **5 tablas de PIB departamental por sector económico** (una por cada uno de los 5 departamentos con proyectos de cobre), no capturadas en ninguna fase anterior — el script extrae específicamente la fila "Explotación de minas y canteras" de esas 5 tablas.

**Hallazgo de esta fase:** la minería representa el **7,2%-11,2% del PIB de Antioquia** (2019-2022) — muy por encima de Chocó (0,9%-2,1%), Córdoba (0,8%-1,7%), Putumayo (1,5%-2,2%) o Santander (3,6%-5,0%). UPME no aclara en el texto de la tabla si el porcentaje es participación en el PIB departamental o en el PIB nacional de esa actividad — se transcribe literal, sin inferir la base de cálculo, y se marca así explícitamente en la salida. Los valores son **idénticos entre la edición 2023 y la 2025** del documento (misma fuente DANE), lo que confirma consistencia entre ambas ediciones.

## 3. Por qué la Fase 3 es "no bloqueante" (honestidad técnica, no limitación oculta)

Ninguna entidad colombiana (ANM, UPME, SGC, ANLA) publica una API de datos abiertos para minería de cobre. Fingir una extracción automática confiable de cifras específicas desde sus páginas HTML sería, en la práctica, un scraper frágil que rompe cada vez que cambian el diseño de la página — y que podría reportar cifras erróneas sin que nadie lo note. En lugar de eso, la Fase 3 hace lo que sí es honesto de automatizar: **detectar cuándo cambia el contenido** (vía hash SHA-256 del texto visible), para alertar "esto se movió, un humano debe revisarlo" en vez de inventar una estructura de datos que esas páginas no tienen.

## 4. Procedencia de los datos (`data/consolidado/dataset_maestro.json`)

Cada bloque del dataset maestro está etiquetado con su origen y nivel de confiabilidad:

| Origen | Significado | Bloques |
|---|---|---|
| `curado_investigacion_humana` | Verificado por lectura directa de fuentes primarias (prensa especializada, comunicados oficiales, papers) | proyectos, demanda global, potencial, estudios científicos |
| `api_publica_en_vivo` | Dato oficial descargado automáticamente en cada corrida, sin intervención humana | precio histórico del cobre (FRED); ficha de cobre del USGS; recursos/reservas por proyecto (UPME) |
| `snapshot_html_sin_api` | Sensor de cambios, no fuente de cifras | páginas de ANM/UPME/SGC/ANLA |
| `estimacion_propia_razonada` | Hipótesis de planificación explícitamente no oficial | KPIs de la hoja de ruta 2026-2050 |
| `aportado_manualmente_por_usuario` | Dato oficial, pero obtenido por descarga manual porque la fuente no ofrece API pública | Excel de IEA Critical Minerals Data Explorer 2026 (Fase 6) |

(El bloque `upme_hallazgos_curados_manualmente` usa `curado_investigacion_humana` explícitamente porque se transcribió a mano — ver sección 2.3.)

Esta distinción existe para que nadie —ni una entidad de gobierno, ni un inversionista, ni una versión futura de este mismo pipeline— confunda una extrapolación con un hecho verificado.

## 5. Cómo ejecutarlo

Requiere **Python ≥3.10** (declarado en `pyproject.toml` — el código usa sintaxis de tipos `list[dict]`/`str | None` que exige esa versión mínima). No requiere `.env` ni claves de API para ninguna fase (ver tabla de la sección 2 — todas son APIs públicas sin autenticación, o ingesta manual en el caso de IEA).

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
make install                                          # o: pip install -r pipeline/requirements.txt
make run                                               # o: python pipeline/run_pipeline.py
```

Salida: `data/live/*.json`, `data/consolidado/dataset_maestro.json`, `pipeline/_out/fase1_reporte_validacion.json`.

## 6. Tests y guardrails (agregado 14-sep-2026, tras una revisión externa)

Hasta esta fecha, el pipeline no tenía ningún test automatizado — cada parser se validaba corriéndolo contra la fuente real y leyendo el resultado a ojo. Una revisión externa preguntó explícitamente "¿cómo sabes que extrae lo correcto?" y la respuesta honesta obligó a construir infraestructura nueva, no solo a explicarla mejor.

**Qué se agregó:**
- `tests/` — 51 tests con `pytest`, uno por función de parseo pura de cada fase (`tests/test_phase{1,2,5,6,7,8,9}_*.py`), contra fixtures de **texto/datos reales** capturados de las fuentes el 14-sep-2026 (`tests/fixtures/`) — no datos sintéticos inventados.
- `pipeline/validaciones/validar_dataset_maestro.py` — un **guardrail de consistencia lógica** que corre al final de `run_pipeline.py`: verifica invariantes que nunca deberían violarse (ningún país con más reservas que el total mundial, el potencial de Colombia no puede exceder las reservas mundiales, el precio del cobre debe estar en un rango físicamente plausible, todo bloque debe tener su etiqueta de procedencia).
- `.github/workflows/test.yml` — corre la batería de tests y el guardrail en cada push/PR, sin red (los tests usan fixtures fijos).

**Lo que este esfuerzo encontró de inmediato (la mejor prueba de que hacía falta):** al construir el fixture de la Fase 5 con el texto real del PDF, se encontró un **segundo bug real y silencioso** que llevaba corriendo sin detectarse desde que se construyó esa fase: Australia mostraba 7.100.000 kt de reservas en vez de 100.000 — un marcador de nota al pie del PDF ("7") pegado al número por la extracción de texto de pdfplumber. Se corrigió con el guardrail genérico (no un parche puntual para Australia), documentado en el propio código de `parsear_tabla_mundial` con la función `_corregir_marcadores_de_nota_al_pie`.

**Límite honesto de estos tests (no resuelto, y no se pretende que lo esté):** los fixtures son una foto fija de las fuentes en sep-2026. Si USGS, UPME o IEA cambian de formato en una edición futura, estos tests **no lo detectan** — seguirán pasando contra el fixture congelado. Lo que sí detectan es una regresión en el código de parseo mismo. La única forma de detectar un cambio de formato real es que la Fase correspondiente falle (o produzca advertencias) al correr contra la fuente en vivo — que es exactamente lo que hace el workflow semanal `actualizar_datos.yml`.

```bash
make install-dev   # o: pip install -r pipeline/requirements-dev.txt
make test            # o: python -m pytest tests/ -v
make validate        # o: python pipeline/validaciones/validar_dataset_maestro.py
```

## 7. Automatización continua (Fase de optimización)

El workflow [`​.github/workflows/actualizar_datos.yml`](../.github/workflows/actualizar_datos.yml) ejecuta el pipeline completo **todos los lunes** vía GitHub Actions y hace commit automático si hay cambios — así el repositorio se mantiene actualizado sin intervención manual, cumpliendo el criterio de optimización pedido: la investigación no se congela en la fecha de esta sesión, sigue viva.

## 9. Resiliencia, observabilidad y paralelización (agregado 15-sep-2026, tras una revisión externa)

Una segunda revisión externa preguntó, en esencia: "¿qué pasa si FRED está
caído o USGS cambia el PDF mañana?", "¿cómo se comparan los cambios
semanales del dataset?", "¿por qué estas decisiones de arquitectura?", y
"¿qué pasa si se agregan las fases 10-15?". Cuatro preguntas, cuatro piezas
de infraestructura nueva:

**1. Reintentos con backoff exponencial** — `pipeline/http_utils.py`
reemplaza las llamadas `requests.get()` directas de las Fases 2, 3, 5, 7, 8
y 9 con `get_con_reintentos()`: 3 intentos con espera exponencial (2s, 4s,
techo 10s) **solo** ante errores transitorios (timeout, error de conexión,
o HTTP 429/5xx) — un 404/403 falla de inmediato porque no es un problema
que un reintento resuelva. Antes de esto, la respuesta honesta a "¿qué pasa
si FRED está caído?" era "la fase falla en el primer intento, sin
reintento, y punto". Verificado con `tests/test_http_utils.py` simulando
ambos escenarios (recuperación al 3er intento, y agotamiento de reintentos)
sin pegarle a la red real.

**2. Logging estructurado y log de ejecución** —
`pipeline/logging_utils.py` reemplaza los `print()` del orquestador
(los `print()` internos de cada fase se mantienen, son para lectura humana
en consola) por el módulo `logging`, y acumula un `RegistroEjecucion` que se
vuelca a `pipeline/_out/ejecucion_log.json` al final de cada corrida —
timestamp, fase, estado (`ok`/`fallo`), duración, y traceback resumido si
falló. Se publica como artefacto de GitHub Actions en cada corrida de
`actualizar_datos.yml` (incluso si el pipeline falla a mitad de camino —
antes, una corrida fallida en CI solo dejaba "Process completed with exit
code 1", sin evidencia de en qué fase ni cuánto tardó cada una hasta ese
punto).

**3. Comparación histórica y detección de anomalías** —
`pipeline/auditoria_semanal/comparar_dataset_maestro.py` archiva cada
corrida en `data/consolidado/historico/dataset_maestro_<AAAA>_W<SS>.json`
(numeración de semana ISO) y compara un conjunto curado de campos numéricos
clave (precio del cobre, CAGR, potencial de Colombia, demanda IEA, % de
Colombia sobre reservas mundiales USGS) contra el snapshot archivado más
reciente. Una variación mayor a 50% en cualquiera de esos campos genera una
alerta en `data/consolidado/_audit_semana_<AAAA>_W<SS>.json` — por ejemplo,
una caída de precio de esa magnitud probablemente sea un error de la fuente,
no un movimiento real de mercado. Es un guardrail de **observabilidad**, no
de validación dura: reporta, no bloquea (a diferencia de
`pipeline/validaciones/validar_dataset_maestro.py`). En la primera corrida
(sin historial todavía) simplemente archiva, sin comparar — probado en
vivo contra el dataset real, incluyendo un caso con una anomalía inyectada
deliberadamente para confirmar que la alerta se dispara (ver
`tests/test_auditoria_semanal.py` para la lógica pura, con fixtures
sintéticos).

**4. Paralelización de fases no bloqueantes** — `run_pipeline.py` corre las
Fases 3, 5, 6, 7, 8 y 9 (independientes entre sí — cada una lee sus propias
fuentes y escribe su propio archivo, sin leer lo que las demás producen)
con `concurrent.futures.ThreadPoolExecutor`, tope de 3 hilos simultáneos
(no ilimitado, para no disparar límites de tasa de las fuentes externas de
golpe). Las Fases 1, 2, 4 y el guardrail final siguen secuenciales por
diseño — ver ADR 001 para el porqué de cada clasificación
bloqueante/no bloqueante. El log de ejecución ahora incluye duración por
fase, verificado en una corrida real completa (ver
`pipeline/_out/ejecucion_log.json` tras `make run`).

**Documentado formalmente en 3 Architecture Decision Records**, para que
decisiones ya tomadas (algunas desde el inicio del proyecto) queden
explícitas y su razonamiento no se pierda con el tiempo:
- [`docs/ADR_001_arquitectura_fases.md`](ADR_001_arquitectura_fases.md) — por qué el pipeline es por fases, y qué cambiaría si ANM/UPME/SGC/ANLA publicaran una API mañana.
- [`docs/ADR_002_fred_price_source.md`](ADR_002_fred_price_source.md) — por qué FRED y no Bloomberg/Refinitiv/LME para el precio del cobre.
- [`docs/ADR_003_parseo_pdf_vs_api_upme.md`](ADR_003_parseo_pdf_vs_api_upme.md) — por qué parsear PDFs de UPME en vez de esperar una API que no existe ni está anunciada.

**Cuándo esto deja de alcanzar (nota de roadmap, no una tarea pendiente
hoy):** un `ThreadPoolExecutor` plano no da reintentos por fase completa,
backfill histórico automático, ni un grafo de dependencias más fino que
"bloqueante antes de la 4, no bloqueante en paralelo". Si el pipeline
creciera a 15+ fases con dependencias reales *entre* fases no bloqueantes
(no solo "todas antes de la 4"), o necesitara reprocesar una ventana
histórica completa, ese es el punto de migrar a **Airflow o Prefect** — no
antes. Introducir un orquestador de ese peso hoy, con 10 fases y una sola
dependencia real (todo antes de la 4), sería complejidad sin necesidad —
exactamente el tipo de sobre-ingeniería que este proyecto ha evitado
deliberadamente en cada fase (ver sección 1: "investigar primero,
automatizar después").

## 10. Próximas fases (roadmap del propio pipeline, no solo del sector)

- ~~**Fase 5:** Fetcher de USGS Mineral Commodity Summaries~~ — **hecho.** Ver `pipeline/phase5_usgs/`.
- ~~**Fase 6:** Integración del IEA Critical Minerals Data Explorer~~ — **hecho, como ingesta manual** (se confirmó que IEA no ofrece API pública ni con cuenta gratuita — ver sección 2.2). Ver `pipeline/phase6_iea/`.
- ~~**Fase 7:** Extracción estructurada de tablas de los PDFs de UPME~~ — **hecho.** Ver `pipeline/phase7_upme_sgc/`.
- ~~**Fase 8:** Serie histórica del USGS Data Series 140~~ — **hecho.** Ver `pipeline/phase8_usgs_historia/` (cobertura 1900-2020).
- ~~**Fase 9:** Auditoría de los 2 documentos de UPME restantes~~ — **hecho, como catálogo (no extracción total).** Ver `pipeline/phase9_upme_auditoria/`. Confirmó que no hay cifras de recursos/reservas sin capturar; sí aportó el PIB minero de los 5 departamentos con proyectos de cobre (hallazgo: Antioquia depende de minería en 7,2%-11,2% de su PIB, muy por encima de los otros 4).
- ~~**Resiliencia/observabilidad:** reintentos, logging estructurado, comparación histórica, paralelización~~ — **hecho.** Ver sección 9.
- **Fase 10 (pendiente):** Extraer las tablas de "Análisis RUNAP" (superposición con áreas protegidas) catalogadas por la Fase 9 en la categoría `ambiental` — relevante para `docs/07-blindaje-social-barranquilla.md` y para evaluar riesgo de licenciamiento de cada proyecto.

---
*Ver también: [Análisis a nivel de artículo científico](10-articulo-analisis-cientifico.md) · [README / dashboard](../README.md)*
