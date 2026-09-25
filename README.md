# 🇨🇴 Colombia · Cobre y Minerales Críticos — Inteligencia 2026–2050

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22814732.svg)](https://doi.org/10.5281/zenodo.22814732)

**Repositorio de investigación estratégica con pipeline de datos ejecutable.** Cobre, minerales críticos, alianza Colombia–EE. UU. y manufactura avanzada global — investigación primero, automatización después.

> Última corrida del pipeline: ver `data/consolidado/dataset_maestro.json → generado_utc` · Curación de investigación: 14-sep-2026 · Release actual: [v1.0.0](https://github.com/wilmerjoseperezorozco-dev/colombia-cobre-minerales-criticos-2050/releases/tag/v1.0.0) · [Changelog](CHANGELOG.md)

## 🔴🟢 Estado del pipeline

| Fase | Script | Última corrida verificada | Resultado real |
|---|---|---|---|
| 1 — Semilla | [`pipeline/phase1_seed/validate_seed.py`](pipeline/phase1_seed/validate_seed.py) | ✅ OK | 7 proyectos validados, 0 errores de esquema |
| 2 — Precio en vivo (FRED) | [`pipeline/phase2_live_fetch/fetch_copper_price_fred.py`](pipeline/phase2_live_fetch/fetch_copper_price_fred.py) | ✅ OK | 415 observaciones (1992→2026); último dato **USD 13.542,82/t** (jul-2026) |
| 3 — Snapshot fuentes oficiales | [`pipeline/phase3_scrape_oficiales/fetch_fuentes_colombianas.py`](pipeline/phase3_scrape_oficiales/fetch_fuentes_colombianas.py) | ✅ OK | ANM, UPME, SGC, ANLA — 5/5 fuentes con HTTP 200 |
| 5 — USGS Mineral Commodity Summaries | [`pipeline/phase5_usgs/fetch_usgs_copper_mcs.py`](pipeline/phase5_usgs/fetch_usgs_copper_mcs.py) | ✅ OK | 18/18 países parseados · reservas mundiales 980.000 kt · **el cobre es mineral crítico de EE. UU. desde el 7-nov-2025** (90 FR 50494) |
| 6 — IEA Critical Minerals (ingesta manual) | [`pipeline/phase6_iea/ingest_iea_manual.py`](pipeline/phase6_iea/ingest_iea_manual.py) | ✅ OK | Demanda oficial 2025: 27.775 kt · brecha oferta-demanda calculada: 6.799 kt (2030) → 17.801 kt (2040) · **reemplazó cifras de prensa no verificadas** |
| 7 — UPME Informe Cobre | [`pipeline/phase7_upme_sgc/fetch_upme_informe_cobre.py`](pipeline/phase7_upme_sgc/fetch_upme_informe_cobre.py) | ✅ OK | 5/5 filas de potencial nacional + recursos/reservas de los 5 proyectos parseados · **corrigió el potencial de Colombia de 9,7 a 17,4 Mt** |
| 8 — USGS histórico (DS140) | [`pipeline/phase8_usgs_historia/fetch_usgs_ds140_copper.py`](pipeline/phase8_usgs_historia/fetch_usgs_ds140_copper.py) | ✅ OK | Serie de EE. UU. **1900-2020** (121 años) resolviendo la URL vigente en tiempo de ejecución |
| 9 — Auditoría UPME (402 pág.) | [`pipeline/phase9_upme_auditoria/audit_upme_docs_adicionales.py`](pipeline/phase9_upme_auditoria/audit_upme_docs_adicionales.py) | ✅ OK | 165-168 tablas catalogadas por documento · 0 recursos/reservas sin capturar · **PIB minero: Antioquia 7,2%-11,2%** vs. 0,8%-2,2% en los otros 4 departamentos |
| 4 — Consolidación | [`pipeline/phase4_consolidacion/build_dataset_maestro.py`](pipeline/phase4_consolidacion/build_dataset_maestro.py) | ✅ OK | `data/consolidado/dataset_maestro.json` — CAGR cobre 5a: **7,46% anual** |

**Ejecutarlo tú mismo:**

```bash
python -m venv .venv && source .venv/bin/activate   # o .venv\Scripts\activate en Windows
make install        # o: pip install -r pipeline/requirements.txt
make run             # o: python pipeline/run_pipeline.py
```

Requiere **Python ≥3.10** (declarado en `pyproject.toml`). No necesita `.env` ni claves de API — ninguna fuente de este pipeline requiere credenciales (ver tabla de fases más abajo). La única excepción es la **Fase 6 (IEA)**, que depende de un archivo que tú mismo descargas manualmente — instrucciones exactas, con hash de verificación, en [`docs/09-metodologia-pipeline.md`](docs/09-metodologia-pipeline.md#22-fase-6-en-detalle--cuando-la-fuente-oficial-no-tiene-api-y-el-usuario-aporta-el-archivo). Las fases 3/5/6/7/8/9 corren en paralelo (máx. 3 hilos a la vez); una corrida completa con re-descarga de todos los PDFs/Excel toma ~2-3 minutos (la Fase 9, que audita 402 páginas combinadas, es el cuello de botella real — medido, no estimado, en `pipeline/_out/ejecucion_log.json`).

**Tests y guardrails (ver sección de garantías de calidad más abajo):**
```bash
make install-dev     # o: pip install -r pipeline/requirements-dev.txt
make test             # o: python -m pytest tests/ -v
make validate         # o: python pipeline/validaciones/validar_dataset_maestro.py
make audit             # o: python pipeline/auditoria_semanal/comparar_dataset_maestro.py
```

Automatizado semanalmente vía [GitHub Actions](.github/workflows/actualizar_datos.yml) (corre el pipeline real) y en cada push/PR vía [`.github/workflows/test.yml`](.github/workflows/test.yml) (corre los tests con fixtures, sin red). Metodología completa en [`docs/09-metodologia-pipeline.md`](docs/09-metodologia-pipeline.md).

## 🛡️ Garantías de calidad: qué se verifica automáticamente y qué no (léase antes de confiar en una cifra)

Esta pregunta se hizo explícitamente durante dos revisiones externas del repositorio (14 y 15-sep-2026) y la respuesta honesta requirió construir infraestructura nueva, no solo explicarla:

| Pregunta | Respuesta |
|---|---|
| ¿Hay tests unitarios por parser? | **Sí** — 59 tests en [`tests/`](tests/), uno por función de parseo, contra fixtures de texto/datos **reales** capturados de las fuentes (no sintéticos inventados) |
| ¿Hay fixtures para detectar cambios de formato de fuente? | Sí, pero con una limitación honesta: los fixtures son una foto fija de la fuente en sep-2026 — **no detectan** que USGS/UPME/IEA cambien de formato en el futuro (para eso está el workflow semanal corriendo la extracción real); **sí detectan** una regresión en el código de parseo |
| ¿La corrección de la Fase 7 (9.7→17.4 Mt) fue manual o hubo guardrails? | **100% manual** en su momento. Al construir los tests de esta sección se encontró un **segundo bug real, silencioso, nunca antes reportado**: Australia mostraba 7.100.000 kt de reservas en vez de 100.000 (un marcador de nota al pie del PDF pegado al número) — corregido con un guardrail genérico (`pipeline/validaciones/validar_dataset_maestro.py`) que ahora corre al final de cada ejecución del pipeline |
| ¿Qué SÍ detecta el guardrail? | Que ningún país tenga más reservas que el total mundial, que el potencial de Colombia no exceda las reservas mundiales, que el precio del cobre esté en un rango físicamente plausible, y que todo bloque tenga su etiqueta de procedencia |
| ¿Qué NO detecta? | Un valor incorrecto pero *consistente* con el resto (ej. un error que afecte igual a dos fuentes relacionadas) — ver limitaciones documentadas en el docstring de `validar_dataset_maestro.py` |
| ¿Si FRED está caído o USGS cambia el PDF mañana, qué pasa? | **Antes (14-sep-2026): la fase fallaba en el primer intento, sin reintento.** Ahora [`pipeline/http_utils.py`](pipeline/http_utils.py) reintenta 3 veces con backoff exponencial ante errores transitorios (timeout/conexión/5xx/429) — no ante 404/403, que son errores de la fuente, no del momento. Verificado con `tests/test_http_utils.py` simulando ambos escenarios sin red real. Si el PDF cambia de formato, la fase falla o emite advertencias explícitas (no bloqueante — ver `docs/ADR_001_arquitectura_fases.md`) y queda registrado en `pipeline/_out/ejecucion_log.json`, publicado como artefacto de CI |
| ¿Cómo se comparan los cambios semanales del dataset? ¿hay historial? | **Antes: se sobrescribía, sin historial.** Ahora [`pipeline/auditoria_semanal/comparar_dataset_maestro.py`](pipeline/auditoria_semanal/comparar_dataset_maestro.py) archiva cada corrida en `data/consolidado/historico/dataset_maestro_<AAAA>_W<SS>.json` y compara 5 campos numéricos clave contra la semana anterior — una variación >50% (ej. una caída fuerte de precio) genera una alerta en `data/consolidado/_audit_semana_<AAAA>_W<SS>.json`. Probado con casos sintéticos y verificado en vivo contra el dataset real con una anomalía inyectada deliberadamente |
| ¿Por qué estas decisiones de arquitectura (fases, FRED, PDFs)? | Documentado formalmente en 3 ADR: [`ADR_001`](docs/ADR_001_arquitectura_fases.md) (arquitectura por fases), [`ADR_002`](docs/ADR_002_fred_price_source.md) (FRED vs. Bloomberg/Refinitiv/LME), [`ADR_003`](docs/ADR_003_parseo_pdf_vs_api_upme.md) (parseo de PDF vs. esperar una API de UPME) |



---

## 🔎 Panorama en una mirada

| Señal | Estado | Fuente |
|---|---|---|
| 🟢 Marco EE. UU.–Colombia de minerales críticos | Firmado 8-sep-2026 en Barranquilla · financiamiento conjunto en 6 meses (vence mar-2027) | [`docs/05-fuentes.md`](docs/05-fuentes.md) |
| 🟢 El cobre es mineral crítico de EE. UU. desde el 7-nov-2025 | Federal Register 90 FR 50494 — explica con fecha exacta el porqué del marco firmado 10 meses después | [`data/live/usgs_copper_mcs.json`](data/live/usgs_copper_mcs.json) |
| 🔴 El Teniente (Chile), jul-2025: 6 muertos por sismicidad inducida | Misma técnica de hundimiento de bloques que Quebradona declara replicar; alertas sísmicas ignoradas deliberadamente | [`docs/12-sismicidad-inducida-y-gemelo-digital.md`](docs/12-sismicidad-inducida-y-gemelo-digital.md) |
| 🟡 Colombia ya tiene sismicidad inducida real desde 2013 (Puerto Gaitán, Meta) | +900 sismos por reinyección de agua petrolera; el propio Ministerio de Minas alegó que su norma "no aplicaba a campos convencionales" — vacío regulatorio documentado | [`docs/12-sismicidad-inducida-y-gemelo-digital.md`](docs/12-sismicidad-inducida-y-gemelo-digital.md#3-corrección-importante-colombia-no-parte-de-cero) |
| 🟡 Proyecto de cobre más avanzado del país (El Alacrán) | Licencia ambiental completa, pero **100% capital chino** desde may-2025 | [`data/proyectos_cobre_colombia.json`](data/proyectos_cobre_colombia.json) |
| 🔴 Quebradona (AngloGold Ashanti, USD 1.400 M) | Frenado por Resolución 855/2025 | [`data/proyectos_cobre_colombia.json`](data/proyectos_cobre_colombia.json) |
| 🟢 Potencial geológico | **17,4 Mt de Cu** en 2 regiones propias (corregido 14-sep-2026, ver nota) · **97% del territorio sin explorar** | [`data/potencial_colombia_y_retos.json`](data/potencial_colombia_y_retos.json) |
| 🔴 Déficit de gobernanza minera | -88% IED minera, -18% PIB minero, 800+ bloqueos, minería ilegal en 29/32 departamentos | [`data/potencial_colombia_y_retos.json`](data/potencial_colombia_y_retos.json) |
| 🟢 Mercado global | Déficit estructural de cobre; hasta 30% de brecha de oferta en 2035 (IEA) | [`data/metricas_demanda_global_cobre.json`](data/metricas_demanda_global_cobre.json) |
| 🟡 Puerto de Barranquilla | Récord mensual: 1,32 Mt en jul-2026; zonas francas del Atlántico +178% desde prepandemia | [`docs/04-estrategia-barranquilla.md`](docs/04-estrategia-barranquilla.md) |
| 🔵 Ventana geopolítica 2027-2032 | Punto de mayor tensión EE. UU.-China (Taiwán/semiconductores) coincide con la maduración de proyectos mineros colombianos | [`docs/13-contexto-geopolitico-2026-2050.md`](docs/13-contexto-geopolitico-2026-2050.md) |

**El hallazgo que más importa de esta investigación:** el único proyecto de cobre a gran escala de Colombia con licencia ambiental completa es, hoy, propiedad 100% de un consorcio chino — exactamente lo contrario del objetivo declarado por el marco firmado con Estados Unidos en Barranquilla apenas unos días antes de esta actualización. Ver detalle en [`docs/01-analisis-ampliado-2026-2050.md`](docs/01-analisis-ampliado-2026-2050.md#1-lo-que-cambió-con-la-investigación-ampliada).

**Corrección de integridad del propio análisis (14-sep-2026):** dos veces en la misma sesión, verificar contra la fuente primaria obligó a corregir una cifra que este repositorio había citado de un resumen de prensa. (1) La Fase 7 encontró que "Colombia tiene 9,7 Mt de cobre dentro de un cinturón de 37,3 Mt" era una interpretación incorrecta de UPME — el potencial real es **17,4 Mt** (dos regiones geológicas propias); 37,3 Mt es el promedio de otras tres regiones *compartidas* con Ecuador, Perú y Panamá. (2) La Fase 6, con el dataset oficial de IEA, encontró que la demanda global de cobre 2025 citada como "34,5 Mtpa" (atribuida a S&P Global/Wood Mackenzie sin verificar) en realidad es **27.775 kt** según la fuente primaria de IEA — la afirmación de que ya había déficit de oferta en 2025 se retracta; el déficit real y bien fundamentado aparece después de 2030. Ambos errores y sus correcciones quedan documentados, no ocultados — ver [`docs/10-articulo-analisis-cientifico.md`](docs/10-articulo-analisis-cientifico.md#35-escala-del-potencial-colombiano-frente-a-las-reservas-mundiales-oficiales).

---

## 🎯 Optimización: las 3 palancas de mayor retorno / menor costo

1. **Unificar los datos ya existentes** (UPME + SGC + ANLA + ANM, hoy dispersos en PDFs y geoportales separados) — es la base de todo lo demás y no requiere esperar ningún proyecto minero.
2. **Mapeo de prospectividad mineral con IA** sobre el 97% del territorio sin explorar, usando datos geológicos que ya existen — ver [`docs/02-ia-medicion-y-formulas.md`](docs/02-ia-medicion-y-formulas.md).
3. **Monitoreo de relaves con InSAR + IA** como condición de licencia desde ya — evita repetir Brumadinho/Mariana y no depende de que madure ningún proyecto.

---

## 📚 Índice del repositorio

| Documento | Contenido |
|---|---|
| [`docs/01-analisis-ampliado-2026-2050.md`](docs/01-analisis-ampliado-2026-2050.md) | Horizonte extendido a 2050, puntos a favor/en contra, brechas de infraestructura |
| [`docs/02-ia-medicion-y-formulas.md`](docs/02-ia-medicion-y-formulas.md) | IA para prospectividad y monitoreo de relaves, fórmulas técnicas (ley de corte, VPN, intensidad de cobre) |
| [`docs/03-estudios-colombia-y-ejecucion.md`](docs/03-estudios-colombia-y-ejecucion.md) | Inventario de estudios científicos colombianos, qué hacer y cómo ejecutarlo |
| [`docs/04-estrategia-barranquilla.md`](docs/04-estrategia-barranquilla.md) | Por qué Barranquilla concentra la visibilidad institucional del marco bilateral, y qué vacíos de mercado deja abiertos |
| [`docs/05-fuentes.md`](docs/05-fuentes.md) | Todas las fuentes consultadas, por categoría |
| [`docs/06-soluciones-juridicas-e-institucionales.md`](docs/06-soluciones-juridicas-e-institucionales.md) | Fallos clave (SU-095/2018, Cajamarca/La Colosa), Decreto 0742/2026 de cierre de minas, pulso estatización vs. desregulación, y la vía más segura y barata |
| [`docs/07-blindaje-social-barranquilla.md`](docs/07-blindaje-social-barranquilla.md) | Caso de alerta (polvo de concentrado en Antofagasta) y el paquete de blindaje social preventivo para el puerto de Barranquilla |
| [`docs/08-oportunidades-inversion.md`](docs/08-oportunidades-inversion.md) | Mapa informativo de empresas públicas con exposición a cobre colombiano (no es asesoría financiera) |
| [`docs/09-metodologia-pipeline.md`](docs/09-metodologia-pipeline.md) | Arquitectura del pipeline por fases, procedencia de datos, cómo ejecutarlo y roadmap de fases futuras |
| [`docs/10-articulo-analisis-cientifico.md`](docs/10-articulo-analisis-cientifico.md) | Análisis con estructura IMRaD (hipótesis, métodos, resultados reproducibles, discusión, limitaciones) |
| [`docs/11-geografia-sitios-candidatos.md`](docs/11-geografia-sitios-candidatos.md) | Dónde está el 97% sin explorar, coordenadas de municipios de referencia, sitios candidatos y no candidatos para fundición-refinería, energía de doble uso |
| [`docs/12-sismicidad-inducida-y-gemelo-digital.md`](docs/12-sismicidad-inducida-y-gemelo-digital.md) | Sismicidad inducida vs. tectónica, el colapso de El Teniente (jul-2025, 6 muertos, misma técnica que Quebradona), comparación regulatoria internacional y propuesta de gemelo digital para Colombia |
| [`docs/13-contexto-geopolitico-2026-2050.md`](docs/13-contexto-geopolitico-2026-2050.md) | Rivalidad entre potencias hasta 2050 (EE. UU.-China, Rusia-OTAN, Irán-Israel), tres escenarios prospectivos, y la posición de Colombia hacia 2030 |
| [`docs/ADR_001_arquitectura_fases.md`](docs/ADR_001_arquitectura_fases.md) | Por qué el pipeline es por fases independientes con bloqueo selectivo, y qué cambiaría si ANM/UPME/SGC/ANLA publicaran una API mañana |
| [`docs/ADR_002_fred_price_source.md`](docs/ADR_002_fred_price_source.md) | Por qué FRED (no Bloomberg/Refinitiv/LME) como fuente del precio histórico del cobre |
| [`docs/ADR_003_parseo_pdf_vs_api_upme.md`](docs/ADR_003_parseo_pdf_vs_api_upme.md) | Por qué parsear los PDFs de UPME en vez de esperar una API que no existe ni está anunciada |
| [`Colombia_Cobre_Mineria_2026-2030.docx`](Colombia_Cobre_Mineria_2026-2030.docx) | Informe original en Word (portada, tablas, hoja de ruta 2026-2030) |

## ⚙️ Pipeline de datos (`/pipeline`)

```
pipeline/
├── phase1_seed/               Valida data/*.json curados contra esquema (bloqueante, secuencial)
├── phase2_live_fetch/         Precio de cobre EN VIVO desde FRED, API pública real (bloqueante, secuencial)
├── phase3_scrape_oficiales/   Snapshot + detección de cambios en ANM/UPME/SGC/ANLA (no bloqueante, paralelo)
├── phase5_usgs/                PDF oficial del USGS parseado: producción/reservas mundiales (no bloqueante, paralelo)
├── phase6_iea/                 Ingesta manual del Excel oficial de IEA: demanda/oferta de cobre (no bloqueante, paralelo)
├── phase7_upme_sgc/            PDF oficial de UPME parseado: potencial nacional + recursos/reservas por proyecto (no bloqueante, paralelo)
├── phase8_usgs_historia/       Serie de EE.UU. 1900-2020, URL resuelta en tiempo de ejecución (no bloqueante, paralelo)
├── phase9_upme_auditoria/      Catálogo de tablas de los 2 PDFs UPME restantes + PIB minero regional (no bloqueante, paralelo)
├── phase4_consolidacion/      Dataset maestro con procedencia + métricas calculadas (bloqueante, corre al final)
├── auditoria_semanal/          Archiva + compara dataset_maestro.json semana a semana, detecta anomalías (no bloqueante)
├── validaciones/                Guardrail de consistencia lógica sobre el dataset final (bloqueante, corre último)
├── http_utils.py                Reintentos con backoff exponencial para toda descarga HTTP del pipeline
├── logging_utils.py             Logging estructurado + pipeline/_out/ejecucion_log.json (timestamp/fase/estado/duración)
└── run_pipeline.py             Orquestador — 1→2 secuencial, luego 3/5/6/7/8/9 en paralelo (ThreadPoolExecutor), luego 4→auditoría→guardrail
```

Cada bloque de [`data/consolidado/dataset_maestro.json`](data/consolidado/dataset_maestro.json) queda etiquetado con su **origen** (`curado_investigacion_humana` / `api_publica_en_vivo` / `snapshot_html_sin_api` / `estimacion_propia_razonada`) para que nunca se confunda una estimación con un dato verificado. Cada corrida semanal se archiva en `data/consolidado/historico/dataset_maestro_<AAAA>_W<SS>.json`, comparada contra la anterior — ver `data/consolidado/_audit_semana_<AAAA>_W<SS>.json` para el reporte de anomalías, si las hubo.

## 🗂️ Datos crudos (`/data`)

Estructurados en JSON para reutilizar en cualquier análisis posterior con IA:

- [`proyectos_cobre_colombia.json`](data/proyectos_cobre_colombia.json) — los 7 proyectos/rondas identificados, con cifras, operador, origen de capital y estado regulatorio.
- [`metricas_demanda_global_cobre.json`](data/metricas_demanda_global_cobre.json) — demanda 2024-2050 por escenario (IEA STEPS/APS/NZE vs. consenso de mercado), precios, intensidad de uso por tecnología.
- [`potencial_colombia_y_retos.json`](data/potencial_colombia_y_retos.json) — potencial geológico, inversión en exploración, impacto de la crisis reciente, minería ilegal, y listas explícitas de puntos a favor/en contra.
- [`estudios_cientificos_colombia.json`](data/estudios_cientificos_colombia.json) — inventario de estudios de UPME, SGC, Universidad Nacional, Universidad de Antioquia y literatura internacional de IA aplicada.
- [`kpis_hoja_de_ruta_2026_2050.json`](data/kpis_hoja_de_ruta_2026_2050.json) — KPIs extendidos con hitos 2035/2040/2050.
- [`coordenadas_municipios_cobre.json`](data/coordenadas_municipios_cobre.json) — coordenadas de referencia de los municipios de los 3 cinturones cupríferos, con la ubicación no verificada marcada explícitamente.
- [`sismicidad_inducida_comparativo_paises.json`](data/sismicidad_inducida_comparativo_paises.json) — caso El Teniente 2025, comparativo regulatorio de 7 países/regiones, y la propuesta de gemelo digital para Colombia.

---

## 🗺️ Organización del proyecto (issues, milestones, citación)

| Elemento | Estado |
|---|---|
| Milestones | [v0.1, v0.2, v0.3 y v1.0 completados](../../milestones?state=closed) · [v2.0 en curso](../../milestones) |
| Issues abiertos | [10 issues reales](../../issues) — investigación, monitoreo regulatorio/de mercado, y expansión a otros minerales críticos |
| Topics | `copper` `critical-minerals` `colombia` `mining` `data-pipeline` `open-data` `energy-transition` `geopolitics` `reproducible-research` `usgs` `iea` `python` |
| Changelog | [`CHANGELOG.md`](CHANGELOG.md) — historial de versiones, hallazgos y correcciones metodológicas |
| Citación | [`CITATION.cff`](CITATION.cff) — botón "Cite this repository" activo en GitHub |
| DOI (Zenodo) | [10.5281/zenodo.22814732](https://doi.org/10.5281/zenodo.22814732) — resuelve siempre a la última versión (v1.0.0) |
| Licencia | [`LICENSE`](LICENSE) — CC BY 4.0 (con excepción explícita para el archivo de IEA) |
| Zenodo/DOI | **Pendiente de decisión** — ver [issue #4](../../issues/4): la integración automática de Zenodo solo archiva repositorios **públicos**; este repo es privado hoy |

**Sobre autoría de la investigación:** este repositorio documenta con fecha (commits, `CITATION.cff`, y en su momento un DOI de Zenodo) el momento en que se realizó este análisis integrado de cobre/minerales críticos en Colombia con pipeline de datos reproducible — útil como registro de prioridad si esta línea de investigación se formaliza más adelante (tesis, paper, propuesta institucional).

## ⚠️ Nota metodológica (leer antes de citar cualquier cifra)

Las cifras de inversión movilizable, las metas intermedias (2028/2030) y las proyecciones de escenario (2035/2040/2050) son **estimaciones razonadas construidas por extrapolación** de datos de proyectos individuales y reportes de mercado citados en las fuentes. **No son cifras oficiales** del Gobierno de Colombia, la ANM ni la UPME, y deben validarse con esas entidades antes de circularse como posición oficial. Los datos de proyectos, marcos institucionales y hechos verificables (fechas, montos de transacciones, licencias otorgadas) sí provienen directamente de las fuentes primarias listadas.
