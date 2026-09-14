# 🇨🇴 Colombia · Cobre y Minerales Críticos — Inteligencia 2026–2050

**Repositorio privado de investigación estratégica con pipeline de datos ejecutable.** Cobre, minerales críticos, alianza Colombia–EE. UU. y manufactura avanzada global — investigación primero, automatización después.

> Última corrida del pipeline: ver `data/consolidado/dataset_maestro.json → generado_utc` · Curación de investigación: 14-sep-2026

## 🔴🟢 Estado del pipeline

| Fase | Script | Última corrida verificada | Resultado real |
|---|---|---|---|
| 1 — Semilla | [`pipeline/phase1_seed/validate_seed.py`](pipeline/phase1_seed/validate_seed.py) | ✅ OK | 7 proyectos validados, 0 errores de esquema |
| 2 — Precio en vivo (FRED) | [`pipeline/phase2_live_fetch/fetch_copper_price_fred.py`](pipeline/phase2_live_fetch/fetch_copper_price_fred.py) | ✅ OK | 415 observaciones (1992→2026); último dato **USD 13.542,82/t** (jul-2026) |
| 3 — Snapshot fuentes oficiales | [`pipeline/phase3_scrape_oficiales/fetch_fuentes_colombianas.py`](pipeline/phase3_scrape_oficiales/fetch_fuentes_colombianas.py) | ✅ OK | ANM, UPME, SGC, ANLA — 5/5 fuentes con HTTP 200 |
| 5 — USGS Mineral Commodity Summaries | [`pipeline/phase5_usgs/fetch_usgs_copper_mcs.py`](pipeline/phase5_usgs/fetch_usgs_copper_mcs.py) | ✅ OK | 18/18 países parseados · reservas mundiales 980.000 kt · **el cobre es mineral crítico de EE. UU. desde el 7-nov-2025** (90 FR 50494) |
| 6 — IEA Critical Minerals (ingesta manual) | [`pipeline/phase6_iea/ingest_iea_manual.py`](pipeline/phase6_iea/ingest_iea_manual.py) | ✅ OK | Demanda oficial 2025: 27.775 kt · brecha oferta-demanda calculada: 6.799 kt (2030) → 17.801 kt (2040) · **reemplazó cifras de prensa no verificadas** |
| 7 — UPME Informe Cobre | [`pipeline/phase7_upme_sgc/fetch_upme_informe_cobre.py`](pipeline/phase7_upme_sgc/fetch_upme_informe_cobre.py) | ✅ OK | 5/5 filas de potencial nacional + recursos/reservas de los 5 proyectos parseados · **corrigió el potencial de Colombia de 9,7 a 17,4 Mt** |
| 4 — Consolidación | [`pipeline/phase4_consolidacion/build_dataset_maestro.py`](pipeline/phase4_consolidacion/build_dataset_maestro.py) | ✅ OK | `data/consolidado/dataset_maestro.json` — CAGR cobre 5a: **7,46% anual** |

**Ejecutarlo tú mismo:** `pip install -r pipeline/requirements.txt && python pipeline/run_pipeline.py` — corre en ~8 segundos. Automatizado semanalmente vía [GitHub Actions](.github/workflows/actualizar_datos.yml). Metodología completa en [`docs/09-metodologia-pipeline.md`](docs/09-metodologia-pipeline.md).

---

## 🔎 Panorama en una mirada

| Señal | Estado | Fuente |
|---|---|---|
| 🟢 Marco EE. UU.–Colombia de minerales críticos | Firmado 8-sep-2026 en Barranquilla · financiamiento conjunto en 6 meses (vence mar-2027) | [`docs/05-fuentes.md`](docs/05-fuentes.md) |
| 🟢 El cobre es mineral crítico de EE. UU. desde el 7-nov-2025 | Federal Register 90 FR 50494 — explica con fecha exacta el porqué del marco firmado 10 meses después | [`data/live/usgs_copper_mcs.json`](data/live/usgs_copper_mcs.json) |
| 🟡 Proyecto de cobre más avanzado del país (El Alacrán) | Licencia ambiental completa, pero **100% capital chino** desde may-2025 | [`data/proyectos_cobre_colombia.json`](data/proyectos_cobre_colombia.json) |
| 🔴 Quebradona (AngloGold Ashanti, USD 1.400 M) | Frenado por Resolución 855/2025 | [`data/proyectos_cobre_colombia.json`](data/proyectos_cobre_colombia.json) |
| 🟢 Potencial geológico | **17,4 Mt de Cu** en 2 regiones propias (corregido 14-sep-2026, ver nota) · **97% del territorio sin explorar** | [`data/potencial_colombia_y_retos.json`](data/potencial_colombia_y_retos.json) |
| 🔴 Déficit de gobernanza minera | -88% IED minera, -18% PIB minero, 800+ bloqueos, minería ilegal en 29/32 departamentos | [`data/potencial_colombia_y_retos.json`](data/potencial_colombia_y_retos.json) |
| 🟢 Mercado global | Déficit estructural de cobre; hasta 30% de brecha de oferta en 2035 (IEA) | [`data/metricas_demanda_global_cobre.json`](data/metricas_demanda_global_cobre.json) |
| 🟡 Puerto de Barranquilla | Récord mensual: 1,32 Mt en jul-2026; zonas francas del Atlántico +178% desde prepandemia | [`docs/04-estrategia-barranquilla.md`](docs/04-estrategia-barranquilla.md) |

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
| [`docs/04-estrategia-barranquilla.md`](docs/04-estrategia-barranquilla.md) | Cómo capitalizar esta situación viviendo en Barranquilla — 3 niveles de esfuerzo/retorno |
| [`docs/05-fuentes.md`](docs/05-fuentes.md) | Todas las fuentes consultadas, por categoría |
| [`docs/06-soluciones-juridicas-e-institucionales.md`](docs/06-soluciones-juridicas-e-institucionales.md) | Fallos clave (SU-095/2018, Cajamarca/La Colosa), Decreto 0742/2026 de cierre de minas, pulso estatización vs. desregulación, y la vía más segura y barata |
| [`docs/07-blindaje-social-barranquilla.md`](docs/07-blindaje-social-barranquilla.md) | Caso de alerta (polvo de concentrado en Antofagasta) y el paquete de blindaje social preventivo para el puerto de Barranquilla |
| [`docs/08-oportunidades-inversion.md`](docs/08-oportunidades-inversion.md) | Mapa informativo de empresas públicas con exposición a cobre colombiano (no es asesoría financiera) |
| [`docs/09-metodologia-pipeline.md`](docs/09-metodologia-pipeline.md) | Arquitectura del pipeline por fases, procedencia de datos, cómo ejecutarlo y roadmap de fases futuras |
| [`docs/10-articulo-analisis-cientifico.md`](docs/10-articulo-analisis-cientifico.md) | Análisis con estructura IMRaD (hipótesis, métodos, resultados reproducibles, discusión, limitaciones) |
| [`Colombia_Cobre_Mineria_2026-2030.docx`](Colombia_Cobre_Mineria_2026-2030.docx) | Informe original en Word (portada, tablas, hoja de ruta 2026-2030) |

## ⚙️ Pipeline de datos (`/pipeline`)

```
pipeline/
├── phase1_seed/               Valida data/*.json curados contra esquema (bloqueante)
├── phase2_live_fetch/         Precio de cobre EN VIVO desde FRED, API pública real (bloqueante)
├── phase3_scrape_oficiales/   Snapshot + detección de cambios en ANM/UPME/SGC/ANLA (best-effort)
├── phase5_usgs/                PDF oficial del USGS parseado: producción/reservas mundiales (best-effort)
├── phase6_iea/                 Ingesta manual del Excel oficial de IEA: demanda/oferta de cobre (IEA no ofrece API pública)
├── phase7_upme_sgc/            PDF oficial de UPME parseado: potencial nacional + recursos/reservas por proyecto (best-effort)
├── phase4_consolidacion/      Dataset maestro con procedencia + métricas calculadas (bloqueante, corre último)
└── run_pipeline.py            Orquestador — corre las fases en orden 1→2→3→5→6→7→4
```

Cada bloque de [`data/consolidado/dataset_maestro.json`](data/consolidado/dataset_maestro.json) queda etiquetado con su **origen** (`curado_investigacion_humana` / `api_publica_en_vivo` / `snapshot_html_sin_api` / `estimacion_propia_razonada`) para que nunca se confunda una estimación con un dato verificado.

## 🗂️ Datos crudos (`/data`)

Estructurados en JSON para reutilizar en cualquier análisis posterior con IA:

- [`proyectos_cobre_colombia.json`](data/proyectos_cobre_colombia.json) — los 7 proyectos/rondas identificados, con cifras, operador, origen de capital y estado regulatorio.
- [`metricas_demanda_global_cobre.json`](data/metricas_demanda_global_cobre.json) — demanda 2024-2050 por escenario (IEA STEPS/APS/NZE vs. consenso de mercado), precios, intensidad de uso por tecnología.
- [`potencial_colombia_y_retos.json`](data/potencial_colombia_y_retos.json) — potencial geológico, inversión en exploración, impacto de la crisis reciente, minería ilegal, y listas explícitas de puntos a favor/en contra.
- [`estudios_cientificos_colombia.json`](data/estudios_cientificos_colombia.json) — inventario de estudios de UPME, SGC, Universidad Nacional, Universidad de Antioquia y literatura internacional de IA aplicada.
- [`kpis_hoja_de_ruta_2026_2050.json`](data/kpis_hoja_de_ruta_2026_2050.json) — KPIs extendidos con hitos 2035/2040/2050.

---

## 🗺️ Organización del proyecto (issues, milestones, citación)

| Elemento | Estado |
|---|---|
| Milestones | [v0.1 y v0.2 completados](../../milestones?state=closed) · [v0.3, v1.0, v2.0 en curso](../../milestones) |
| Issues abiertos | [14 issues reales](../../issues) — pipeline, investigación, monitoreo regulatorio/de mercado, y la ruta a Zenodo |
| Topics | `copper` `critical-minerals` `colombia` `mining` `data-pipeline` `open-data` `energy-transition` `geopolitics` `reproducible-research` `usgs` `iea` `python` |
| Citación | [`CITATION.cff`](CITATION.cff) — listo para que GitHub muestre el botón "Cite this repository" |
| Licencia | [`LICENSE`](LICENSE) — CC BY 4.0 (con excepción explícita para el archivo de IEA) |
| Zenodo/DOI | **Pendiente de decisión** — ver [issue #4](../../issues/4): la integración automática de Zenodo solo archiva repositorios **públicos**; este repo es privado hoy |

**Sobre autoría de la investigación:** este repositorio documenta con fecha (commits, `CITATION.cff`, y en su momento un DOI de Zenodo) el momento en que se realizó este análisis integrado de cobre/minerales críticos en Colombia con pipeline de datos reproducible — útil como registro de prioridad si esta línea de investigación se formaliza más adelante (tesis, paper, propuesta institucional).

## ⚠️ Nota metodológica (leer antes de citar cualquier cifra)

Las cifras de inversión movilizable, las metas intermedias (2028/2030) y las proyecciones de escenario (2035/2040/2050) son **estimaciones razonadas construidas por extrapolación** de datos de proyectos individuales y reportes de mercado citados en las fuentes. **No son cifras oficiales** del Gobierno de Colombia, la ANM ni la UPME, y deben validarse con esas entidades antes de circularse como posición oficial. Los datos de proyectos, marcos institucionales y hechos verificables (fechas, montos de transacciones, licencias otorgadas) sí provienen directamente de las fuentes primarias listadas.
