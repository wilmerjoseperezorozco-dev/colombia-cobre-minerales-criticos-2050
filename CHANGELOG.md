# Changelog

Formato inspirado en [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), adaptado a un proyecto de investigación con pipeline de datos (las entradas incluyen tanto código como hallazgos de investigación y correcciones metodológicas). Versionado según [SemVer](https://semver.org/).

> Nota de honestidad metodológica: varias versiones agrupan varios commits del mismo día de trabajo intensivo — las fechas no siempre corresponden a un tag de git formal anterior a v0.3.0 (el primer release etiquetado del repositorio fue `v0.3.0`, el 17-sep-2026). El detalle completo de cada cambio está en el historial de git.

## [1.0.0] — 2026-09-25

Primer release marcado como versión estable del proyecto: cierre de los dos milestones de organización (`v0.3` y `v1.0`), con el pipeline, la investigación y la infraestructura de citación ya verificados en producción durante más de una semana de corridas automáticas reales.

### Added
- Este archivo (`CHANGELOG.md`).

### Fixed
- **Verificación de la cifra de inversión anómala de El Roble** (Tabla 28 del informe UPME, USD 9.475 millones): se confirmó que la transcripción es exacta contra la fuente primaria, que el valor es internamente consistente con el resto de la tabla, y que no existe una corrección disponible en los otros informes de UPME ya integrados al repositorio. Se documenta una hipótesis razonada (valor económico acumulado, no capex comparable) explícitamente marcada como no confirmada por UPME. Ver `data/upme_informe_cobre_hallazgos_curados.json`.

### Verified in production
- El workflow semanal (`actualizar_datos.yml`) corrió de forma autónoma el 21-sep-2026 (semana ISO 2026-W39): las 9 fases, el guardrail y la auditoría histórica se ejecutaron sin intervención humana, archivaron el snapshot semanal y no detectaron anomalías en los 5 campos clave monitoreados — primera confirmación real (no solo en tests) de que la infraestructura de resiliencia y observabilidad agregada en `0.3.0` funciona en las condiciones para las que se diseñó.

## [0.3.0] — 2026-09-17

### Added
- **Fase 8** — serie histórica de producción de cobre en EE. UU. desde 1900 (USGS Data Series 140), con resolución de la URL del Excel vigente en tiempo de ejecución.
- **Fase 9** — auditoría por catálogo de los 2 documentos de UPME restantes (402 páginas combinadas) más el PIB minero por departamento.
- `docs/11-geografia-sitios-candidatos.md` — localización del 97% del territorio sin explorar, coordenadas de municipios, sitios candidatos y no candidatos para fundición-refinería.
- `docs/12-sismicidad-inducida-y-gemelo-digital.md` — sismicidad inducida vs. tectónica, el colapso de El Teniente (jul-2025), y una propuesta de gemelo digital para Colombia, validada posteriormente contra un caso real ya operando en Colombia desde 2013 (Puerto Gaitán, Meta).
- `docs/13-contexto-geopolitico-2026-2050.md` — rivalidad entre potencias hasta 2050 y la posición de Colombia hacia 2030.
- 59 tests automatizados (`tests/`) contra fixtures de datos reales, y un guardrail de consistencia lógica (`pipeline/validaciones/`) que corre al final de cada ejecución del pipeline.
- `pipeline/http_utils.py` — reintentos con backoff exponencial ante fallos transitorios de red, en las 6 fases que descargan de fuentes externas.
- `pipeline/logging_utils.py` — logging estructurado y `pipeline/_out/ejecucion_log.json` (timestamp/fase/estado/duración/excepción), publicado como artefacto de CI en cada corrida.
- `pipeline/auditoria_semanal/` — archivado histórico semanal del dataset maestro (numeración ISO de semana) y comparación automática con detección de anomalías (variación >50% en campos clave).
- Paralelización de las fases no bloqueantes (3, 5, 6, 7, 8, 9) con `concurrent.futures.ThreadPoolExecutor`.
- 3 Architecture Decision Records (`docs/ADR_001` a `ADR_003`) documentando por qué el pipeline es por fases, por qué FRED como fuente de precio, y por qué parsear PDFs de UPME en vez de esperar una API.
- Organización avanzada del repositorio: `CITATION.cff`, `LICENSE` (CC-BY-4.0 con excepción para el archivo de IEA), topics, labels, milestones e issues de seguimiento.
- Integración con Zenodo: repositorio pasado a público (17-sep-2026) y primer DOI generado (`10.5281/zenodo.22814733`, DOI conceptual `10.5281/zenodo.22814732`).

### Changed
- `docs/04-estrategia-barranquilla.md` reescrito de raíz: se retiró todo el contenido de estrategia personal de inversión/negocio y las referencias a proyectos no relacionados con esta investigación, dejando un enfoque puramente investigativo sobre el rol institucional de Barranquilla en el marco bilateral.

### Fixed
- **Bug de marcador de nota al pie** en la tabla mundial del USGS: Australia mostraba 7.100.000 kt de reservas en vez de 100.000 kt (un "7" de nota al pie pegado al número por la extracción de texto de pdfplumber) — corregido con un guardrail genérico, no un parche puntual.
- **Valor hardcodeado desactualizado**: el cálculo de la participación de Colombia sobre las reservas mundiales (Fase 5) seguía usando el potencial geológico ya corregido en otra parte del repositorio (9,7 Mt) en vez del valor real (17,4 Mt) — corregido leyendo el valor desde la fuente única de verdad (`data/potencial_colombia_y_retos.json`).

## [0.2.0] — 2026-09-14

### Added
- **Fase 5** — extracción y parseo en vivo del USGS Mineral Commodity Summaries (Copper): producción y reservas mundiales, designación de mineral crítico de EE. UU.
- **Fase 6** — ingesta manual del IEA Critical Minerals Data Explorer 2026 (IEA no ofrece API pública ni con cuenta gratuita).
- **Fase 7** — informe técnico de UPME: potencial nacional y recursos/reservas por proyecto (El Roble, Quebradona, Soto Norte, Mocoa, San Matías).
- `CITATION.cff`, `LICENSE`, topics, labels, milestones y los primeros 14 issues de seguimiento del repositorio.

### Fixed
- **Corrección de integridad #1** (Fase 7): el potencial geológico de Colombia estaba citado incorrectamente como "9,7 Mt dentro de un cinturón de 37,3 Mt" — verificado contra la fuente primaria de UPME, el potencial real es **17,4 Mt** (dos regiones geológicas propias); 37,3 Mt es el promedio de tres regiones compartidas con Ecuador, Perú y Panamá.
- **Corrección de integridad #2** (Fase 6): la demanda global de cobre 2025 citada como "34,5 Mtpa" (atribuida de forma imprecisa a un resumen de prensa) se reemplazó por la cifra oficial de IEA, **27.775 kt** — esto también retractó la afirmación de que ya existía un déficit de oferta observable en 2025; el déficit real y mejor fundamentado aparece después de 2030.

## [0.1.0] — 2026-09-14

### Added
- Investigación inicial: análisis estratégico sobre cobre y minerales críticos en Colombia, en el contexto de la alianza con Estados Unidos (2026-2050).
- Pipeline de datos ejecutable, fases 1-4: validación del dataset semilla, precio de cobre en vivo (FRED), snapshot de fuentes oficiales colombianas, y consolidación del dataset maestro con procedencia por bloque.
- Análisis con estructura de artículo científico (IMRaD): hipótesis, métodos, resultados reproducibles, discusión y limitaciones.
- Soluciones jurídicas e institucionales, blindaje social preventivo para el puerto de Barranquilla, y mapa informativo de oportunidades de inversión.

---
*Ver también: [README](README.md) · [Metodología del pipeline](docs/09-metodologia-pipeline.md)*
