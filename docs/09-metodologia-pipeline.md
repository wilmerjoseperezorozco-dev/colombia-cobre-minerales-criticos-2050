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

### 2.3 Fase 7 en detalle — el informe técnico UPME y una lección de infraestructura de datos

`pipeline/phase7_upme_sgc/fetch_upme_informe_cobre.py` descarga y parsea el informe técnico "Informe Cobre" de la Subdirección de Minería de UPME (~95 páginas), la fuente con más tablas de recursos/reservas (NI 43-101/JORC/SAMREC) de todo el corpus consultado.

**Hallazgo de infraestructura verificado con DNS-over-HTTPS:** la URL que cita el propio documento en su bibliografía (`www1.upme.gov.co/...`) **no resuelve en DNS público** (`Status: NXDOMAIN` consultado directamente contra `dns.google`, no solo un fallo de este entorno). El dominio operativo real migró a `docs.upme.gov.co` (sitio reconstruido en WordPress). Este script usa la URL que efectivamente responde HTTP 200, documentando la discrepancia — un ejemplo concreto, no anecdótico, de la brecha de acceso a datos oficiales colombianos que `docs/03-estudios-colombia-y-ejecucion.md` ya señalaba de forma general.

**Corrección metodológica que produjo esta fase:** al verificar contra el texto original la cifra "9,7 Mt de un cinturón de 37,3 Mt" que este repositorio había repetido desde la sesión anterior, se encontró que la interpretación era incorrecta — ver el detalle completo en `docs/10-articulo-analisis-cientifico.md`, sección 3.5. El potencial correcto de Colombia es **17,4 Mt** (dos regiones geológicas propias). Esto se corrigió en `data/potencial_colombia_y_retos.json`, `data/estudios_cientificos_colombia.json`, `data/kpis_hoja_de_ruta_2026_2050.json` y en los documentos `01`, `03` y `10`.

**Qué se automatizó vs. qué se transcribió a mano:** las tablas de recursos/reservas por proyecto (Tablas 1-8 del documento) tienen texto lineal parseable con expresiones regulares, aunque con un reto real — pdfplumber extrae las etiquetas de categoría (ej. "Recursos Medidos") partidas alrededor de la fila numérica en vez de antes de ella, por el ajuste de línea de la celda PDF original; el script maneja esto explícitamente. La Tabla 28 (comparativo económico) tiene encabezados rotados 90° que pdfplumber invierte carácter por carácter — ahí se optó por transcripción manual con cita de página exacta, en `data/upme_informe_cobre_hallazgos_curados.json`, en vez de forzar un parseo frágil.

### 2.4 Fase 8 en detalle — resolver la URL en tiempo de ejecución, no hardcodearla

`pipeline/phase8_usgs_historia/fetch_usgs_ds140_copper.py` descarga la serie histórica de cobre de EE. UU. desde 1900 (USGS Data Series 140). A diferencia de la Fase 5 (URL con patrón predecible `mcs{año}-copper.pdf`), el archivo real de esta fase vive en un bucket S3 con nombre versionado (`ds140-copper-2020.xlsx`) enlazado desde una página HTML de aterrizaje — si USGS publica una actualización, el nombre del archivo cambiará (ej. a `ds140-copper-2023.xlsx`). Por eso el script **no hardcodea el nombre del archivo**: descarga primero la página HTML y extrae con una expresión regular el enlace `.xlsx` vigente, luego descarga ese archivo. Esto es más robusto que la Fase 5 frente a actualizaciones de la fuente, al costo de una dependencia adicional (que la página HTML mantenga el mismo patrón de enlace).

**Qué complementa:** la Fase 2 (FRED) cubre precio mensual 1992-2026; esta fase aporta 92 años adicionales (1900-2020) de producción primaria/secundaria de EE. UU., comercio exterior, consumo, valor unitario nominal y ajustado por inflación (dólares de 1998), y producción mundial — con esto, cualquier afirmación sobre "precios históricamente altos" en `docs/10-articulo-analisis-cientifico.md` puede contrastarse contra más de un siglo de datos, no solo contra los últimos 33 años.

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

```bash
pip install -r pipeline/requirements.txt
python pipeline/run_pipeline.py
```

Salida: `data/live/*.json`, `data/consolidado/dataset_maestro.json`, `pipeline/_out/fase1_reporte_validacion.json`.

## 6. Automatización continua (Fase de optimización)

El workflow [`​.github/workflows/actualizar_datos.yml`](../.github/workflows/actualizar_datos.yml) ejecuta el pipeline completo **todos los lunes** vía GitHub Actions y hace commit automático si hay cambios — así el repositorio se mantiene actualizado sin intervención manual, cumpliendo el criterio de optimización pedido: la investigación no se congela en la fecha de esta sesión, sigue viva.

## 7. Próximas fases (roadmap del propio pipeline, no solo del sector)

- ~~**Fase 5:** Fetcher de USGS Mineral Commodity Summaries~~ — **hecho.** Ver `pipeline/phase5_usgs/`.
- ~~**Fase 6:** Integración del IEA Critical Minerals Data Explorer~~ — **hecho, como ingesta manual** (se confirmó que IEA no ofrece API pública ni con cuenta gratuita — ver sección 2.2). Ver `pipeline/phase6_iea/`.
- ~~**Fase 7:** Extracción estructurada de tablas de los PDFs de UPME~~ — **hecho.** Ver `pipeline/phase7_upme_sgc/`.
- ~~**Fase 8:** Serie histórica del USGS Data Series 140~~ — **hecho.** Ver `pipeline/phase8_usgs_historia/` (cobertura 1900-2020).
- **Fase 9 (pendiente):** Repetir el ejercicio de verificación de la Fase 7 sobre los otros dos documentos de UPME identificados y ya localizados con URL funcional en `docs/05-fuentes.md` (`Documento_Cobre_29-12-2023.pdf`, 240 págs., y `Definitivo_Caracterizacion...2025.pdf`, 162 págs.) — se inspeccionaron manualmente durante la construcción de esta fase pero no se dejaron cacheados en el repositorio por su peso (15 MB y 5,7 MB) sin que un script los gestione todavía; ambos son mayormente análisis social/demográfico por municipio, de menor densidad numérica que el Informe Cobre.

---
*Ver también: [Análisis a nivel de artículo científico](10-articulo-analisis-cientifico.md) · [README / dashboard](../README.md)*
