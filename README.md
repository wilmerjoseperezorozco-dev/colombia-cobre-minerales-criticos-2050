# 🇨🇴 Colombia · Cobre y Minerales Críticos — Inteligencia 2026–2050

**Repositorio privado de investigación estratégica.** Cobre, minerales críticos, alianza Colombia–EE. UU. y manufactura avanzada global, con foco en visibilidad institucional y optimización de decisiones.

> Última actualización de datos: **14 de septiembre de 2026**

---

## 🔎 Panorama en una mirada

| Señal | Estado | Fuente |
|---|---|---|
| 🟢 Marco EE. UU.–Colombia de minerales críticos | Firmado 8-sep-2026 en Barranquilla · financiamiento conjunto en 6 meses (vence mar-2027) | [`docs/05-fuentes.md`](docs/05-fuentes.md) |
| 🟡 Proyecto de cobre más avanzado del país (El Alacrán) | Licencia ambiental completa, pero **100% capital chino** desde may-2025 | [`data/proyectos_cobre_colombia.json`](data/proyectos_cobre_colombia.json) |
| 🔴 Quebradona (AngloGold Ashanti, USD 1.400 M) | Frenado por Resolución 855/2025 | [`data/proyectos_cobre_colombia.json`](data/proyectos_cobre_colombia.json) |
| 🟢 Potencial geológico | 9,7 Mt de Cu en un cinturón andino de 37,3 Mt · **97% del territorio sin explorar** | [`data/potencial_colombia_y_retos.json`](data/potencial_colombia_y_retos.json) |
| 🔴 Déficit de gobernanza minera | -88% IED minera, -18% PIB minero, 800+ bloqueos, minería ilegal en 29/32 departamentos | [`data/potencial_colombia_y_retos.json`](data/potencial_colombia_y_retos.json) |
| 🟢 Mercado global | Déficit estructural de cobre; hasta 30% de brecha de oferta en 2035 (IEA) | [`data/metricas_demanda_global_cobre.json`](data/metricas_demanda_global_cobre.json) |
| 🟡 Puerto de Barranquilla | Récord mensual: 1,32 Mt en jul-2026; zonas francas del Atlántico +178% desde prepandemia | [`docs/04-estrategia-barranquilla.md`](docs/04-estrategia-barranquilla.md) |

**El hallazgo que más importa de esta investigación:** el único proyecto de cobre a gran escala de Colombia con licencia ambiental completa es, hoy, propiedad 100% de un consorcio chino — exactamente lo contrario del objetivo declarado por el marco firmado con Estados Unidos en Barranquilla apenas unos días antes de esta actualización. Ver detalle en [`docs/01-analisis-ampliado-2026-2050.md`](docs/01-analisis-ampliado-2026-2050.md#1-lo-que-cambió-con-la-investigación-ampliada).

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
| [`Colombia_Cobre_Mineria_2026-2030.docx`](Colombia_Cobre_Mineria_2026-2030.docx) | Informe original en Word (portada, tablas, hoja de ruta 2026-2030) |

## 🗂️ Datos crudos (`/data`)

Estructurados en JSON para reutilizar en cualquier análisis posterior con IA:

- [`proyectos_cobre_colombia.json`](data/proyectos_cobre_colombia.json) — los 7 proyectos/rondas identificados, con cifras, operador, origen de capital y estado regulatorio.
- [`metricas_demanda_global_cobre.json`](data/metricas_demanda_global_cobre.json) — demanda 2024-2050 por escenario (IEA STEPS/APS/NZE vs. consenso de mercado), precios, intensidad de uso por tecnología.
- [`potencial_colombia_y_retos.json`](data/potencial_colombia_y_retos.json) — potencial geológico, inversión en exploración, impacto de la crisis reciente, minería ilegal, y listas explícitas de puntos a favor/en contra.
- [`estudios_cientificos_colombia.json`](data/estudios_cientificos_colombia.json) — inventario de estudios de UPME, SGC, Universidad Nacional, Universidad de Antioquia y literatura internacional de IA aplicada.
- [`kpis_hoja_de_ruta_2026_2050.json`](data/kpis_hoja_de_ruta_2026_2050.json) — KPIs extendidos con hitos 2035/2040/2050.

---

## ⚠️ Nota metodológica (leer antes de citar cualquier cifra)

Las cifras de inversión movilizable, las metas intermedias (2028/2030) y las proyecciones de escenario (2035/2040/2050) son **estimaciones razonadas construidas por extrapolación** de datos de proyectos individuales y reportes de mercado citados en las fuentes. **No son cifras oficiales** del Gobierno de Colombia, la ANM ni la UPME, y deben validarse con esas entidades antes de circularse como posición oficial. Los datos de proyectos, marcos institucionales y hechos verificables (fechas, montos de transacciones, licencias otorgadas) sí provienen directamente de las fuentes primarias listadas.
