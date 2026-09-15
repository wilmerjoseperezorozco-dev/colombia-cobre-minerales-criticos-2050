# ADR 003 — Parseo estructurado de PDFs de UPME en vez de esperar una API

- **Estado:** Aceptado
- **Fecha:** 2026-09-15 (decisión original tomada al construir la Fase 7; documentada formalmente aquí tras una revisión externa)

## Contexto

UPME (Unidad de Planeación Minero Energética) publica sus informes técnicos
de cobre — incluido el documento con las cifras de recursos/reservas por
proyecto que corrige el error de interpretación 9.7→17.4 Mt documentado en
`docs/01-analisis-ampliado-2026-2050.md` — exclusivamente como **PDF**, sin
ninguna API de datos abiertos ni endpoint JSON/CSV equivalente. Esto se
verificó de forma activa, no se asumió: se intentó resolver
`www1.upme.gov.co` (el dominio citado en referencias bibliográficas más
antiguas) y devolvió `NXDOMAIN` vía consulta DNS-over-HTTPS directa a
`dns.google` — el dominio vigente real es `docs.upme.gov.co`. Ese hallazgo
en sí mismo (un dominio institucional roto en referencias públicas) es
parte de la motivación de este ADR: no hay evidencia de que UPME vaya a
publicar una API en un horizonte razonable, cuando ni siquiera mantiene
consistentes sus URLs de documentos estáticos.

## Opciones consideradas

1. **Esperar/pedir una API de UPME** — descartada. No hay indicio público
   de que esté planeada, y bloquear el pipeline a una promesa de terceros
   sin fecha va en contra del principio operativo de este proyecto
   ("investigar primero, automatizar después" — ver
   `docs/09-metodologia-pipeline.md` sección 1). Una fase que no puede
   correr no aporta nada, con o sin justificación.
2. **Transcripción 100% manual de cada cifra** — descartada como método
   principal (aunque sí se usa como respaldo puntual, ver
   `upme_hallazgos_curados_manualmente` en el dataset maestro). No escala:
   el informe de recursos/reservas por proyecto tiene 5 proyectos con
   estructuras de tabla distintas cada uno (`parsear_el_roble`,
   `parsear_quebradona`, `parsear_soto_norte`, `parsear_mocoa`,
   `parsear_san_matias` en `pipeline/phase7_upme_sgc/fetch_upme_informe_cobre.py`),
   y los documentos de auditoría de la Fase 9 tienen 240-402 páginas
   combinadas — inviable de re-transcribir a mano en cada actualización.
3. **Parseo estructurado del PDF con `pdfplumber` + reglas por función** —
   **elegida**. UPME mantiene un formato tabular razonablemente consistente
   dentro de cada documento (no entre documentos distintos, cada uno tiene
   su propio parser) — condición suficiente para que reglas de extracción
   con regex sean confiables mientras el formato no cambie, con el riesgo
   documentado explícitamente en vez de ocultado.

## Decisión

Se parsean los PDFs de UPME con `pdfplumber`, separando siempre **función
pura de parseo** (recibe texto ya extraído, retorna `dict`) de **función de
I/O** (descarga + cachea el PDF crudo en `pipeline/_out/` para auditoría).
Esta separación —no el parseo en sí— es la parte de la decisión que más
paga en el tiempo: permitió escribir 51+ tests contra fixtures de texto
real sin red (`tests/fixtures/upme_informe_cobre_texto_real.py`), y ya
atrapó un bug real y silencioso (ver sección 6 de
`docs/09-metodologia-pipeline.md`: el marcador de nota al pie "7" pegado al
100.000 de reservas de Australia en la tabla del USGS — mismo patrón de
riesgo que aplica a cualquier PDF, incluidos los de UPME).

## Mitigación del riesgo aceptado (el PDF puede cambiar de formato)

- Cada función de parseo reporta `advertencias` explícitas en vez de fallar
  en silencio cuando una fila esperada no aparece (ver
  `parsear_tabla_mundial` y su guardrail `_corregir_marcadores_de_nota_al_pie`
  en la Fase 5, que sigue el mismo patrón).
- La Fase 7 se declara **no bloqueante** (ADR 001) — un cambio de formato
  rompe esa fase específica, se reporta en el log de ejecución
  (`pipeline/_out/ejecucion_log.json`, ver `pipeline/logging_utils.py`), y
  no tumba el resto del pipeline.
- El PDF crudo se cachea en `pipeline/_out/` en cada corrida — si el
  parseo empieza a fallar, hay evidencia inmediata del documento exacto
  contra el que falló, sin depender de que UPME mantenga versiones
  anteriores accesibles.
- El guardrail `pipeline/validaciones/validar_dataset_maestro.py` contrasta
  el potencial de Colombia salido de UPME contra las reservas mundiales
  del USGS (`validar_potencial_colombia_no_excede_reservas_mundiales`) —
  una corrupción de parseo que produjera un número absurdo (como el bug de
  Australia) tiene una segunda oportunidad de detectarse aquí, no solo en
  el parser de origen.

## Consecuencias

**Positivas:**
- El pipeline no depende de que UPME cambie su infraestructura de
  publicación — funciona con lo que UPME efectivamente publica hoy.
- El patrón (función pura + fixture real + guardrail de plausibilidad) ya
  demostró encontrar errores reales que una revisión manual del "18/18
  países parseados" no había detectado — más confiable que confiar en que
  el parseo "se ve bien" a simple vista.

**Negativas (aceptadas conscientemente):**
- Mantenimiento reactivo: si UPME rediseña un PDF, el parser correspondiente
  se rompe hasta que alguien lo actualice — no hay forma de anticipar ese
  cambio, solo de detectarlo rápido (fallo reportado, no silencioso).
- Cinco funciones de parseo distintas para cinco proyectos con estructuras
  de tabla distintas es más código que un único parser genérico — se
  aceptó ese costo porque un parser "genérico" sobre 5 formatos reales
  distintos tiende a ser más fragil que 5 parsers específicos, cada uno
  simple y testeable por separado.
