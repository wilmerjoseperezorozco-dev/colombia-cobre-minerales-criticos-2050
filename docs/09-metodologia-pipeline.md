# Metodología del pipeline de datos

## 1. Filosofía: investigar primero, automatizar después

El orden de construcción de este repositorio fue deliberado: primero la investigación humana curada (sesiones 1-2, con verificación cruzada de fuentes), y solo después la automatización. Automatizar sin haber investigado primero produce pipelines que extraen datos sin criterio para interpretarlos; investigar sin después automatizar produce un informe estático que se desactualiza en semanas. Este pipeline es el punto donde ambos se encuentran.

## 2. Arquitectura por fases

```
pipeline/
├── phase1_seed/               Valida el dataset curado a mano (bloqueante)
├── phase2_live_fetch/         Extrae datos en vivo de APIs públicas reales (bloqueante)
├── phase3_scrape_oficiales/   Snapshot de páginas oficiales colombianas sin API (no bloqueante)
├── phase4_consolidacion/      Une todo en un dataset maestro con procedencia (bloqueante)
├── schema/                    Esquemas JSON de validación
└── run_pipeline.py            Orquestador — corre las 4 fases en orden
```

| Fase | Qué hace | Tipo de fuente | Bloqueante |
|---|---|---|---|
| 1 — Semilla | Valida `data/*.json` curados por investigación humana contra un esquema | Investigación manual verificada | Sí |
| 2 — Extracción en vivo | Descarga la serie histórica de precio del cobre desde FRED (API pública, sin key) | API pública real | Sí |
| 3 — Snapshot oficial | Descarga el HTML de ANM/UPME/SGC/ANLA y detecta cambios por hash | Páginas oficiales sin API | No (best-effort) |
| 4 — Consolidación | Une fases 1-3 en `data/consolidado/dataset_maestro.json`, marcando el origen y confiabilidad de cada bloque, y calcula métricas derivadas (CAGR, volatilidad) | — | Sí |

## 3. Por qué la Fase 3 es "no bloqueante" (honestidad técnica, no limitación oculta)

Ninguna entidad colombiana (ANM, UPME, SGC, ANLA) publica una API de datos abiertos para minería de cobre. Fingir una extracción automática confiable de cifras específicas desde sus páginas HTML sería, en la práctica, un scraper frágil que rompe cada vez que cambian el diseño de la página — y que podría reportar cifras erróneas sin que nadie lo note. En lugar de eso, la Fase 3 hace lo que sí es honesto de automatizar: **detectar cuándo cambia el contenido** (vía hash SHA-256 del texto visible), para alertar "esto se movió, un humano debe revisarlo" en vez de inventar una estructura de datos que esas páginas no tienen.

## 4. Procedencia de los datos (`data/consolidado/dataset_maestro.json`)

Cada bloque del dataset maestro está etiquetado con su origen y nivel de confiabilidad:

| Origen | Significado | Bloques |
|---|---|---|
| `curado_investigacion_humana` | Verificado por lectura directa de fuentes primarias (prensa especializada, comunicados oficiales, papers) | proyectos, demanda global, potencial, estudios científicos |
| `api_publica_en_vivo` | Dato oficial descargado automáticamente en cada corrida, sin intervención humana | precio histórico del cobre (FRED) |
| `snapshot_html_sin_api` | Sensor de cambios, no fuente de cifras | páginas de ANM/UPME/SGC/ANLA |
| `estimacion_propia_razonada` | Hipótesis de planificación explícitamente no oficial | KPIs de la hoja de ruta 2026-2050 |

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

- **Fase 5 (pendiente):** Fetcher de USGS Mineral Commodity Summaries (dataset público, requiere manejo de PDF/CSV según año de publicación).
- **Fase 6 (pendiente):** Integración de un fetcher para el IEA Critical Minerals Data Explorer si se obtiene una clave de API institucional.
- **Fase 7 (pendiente):** Extracción estructurada de tablas de los PDFs de UPME/SGC ya identificados en `docs/05-fuentes.md`, usando `pdfplumber` (ya incluido en `requirements.txt`), evaluando cada tabla manualmente antes de incorporarla al dataset maestro.

---
*Ver también: [Análisis a nivel de artículo científico](10-articulo-analisis-cientifico.md) · [README / dashboard](../README.md)*
