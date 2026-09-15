# Análisis ampliado: cobre y minerales críticos en Colombia, 2026–2050

> Extiende el informe original (`Colombia_Cobre_Mineria_2026-2030.docx`) con horizonte a 2050, hallazgos nuevos de investigación (sep-2026) y un balance explícito de puntos a favor y en contra. Datos crudos en [`/data`](../data).

## 1. Lo que cambió con la investigación ampliada

Cuatro hallazgos nuevos, no incluidos en la primera versión del informe, cambian la lectura estratégica:

1. **El proyecto de cobre más avanzado de Colombia es de capital chino.** El Alacrán (Córdoba), el único proyecto de cobre a gran escala con licencia ambiental completa en el país, es operado por CMH Colombia, controlada por la china JCHX Mining Management Co., que en mayo de 2025 compró el 50% restante a la canadiense Cordoba Minerals por USD 128 millones. Esto es una tensión directa con el objetivo explícito del marco EE. UU.–Colombia firmado en Barranquilla: reducir la dependencia de China en minerales críticos.
2. **El gobierno ya amplió el objetivo más allá del cobre.** El 4 de septiembre de 2026 Colombia anunció una apuesta explícita también por níquel y tungsteno, con presupuesto de exploración actual de USD 90 M/año y potencial de USD 500 M/año con respaldo estatal.
3. **UPME/USGS cuantificó el potencial real:** Colombia tiene dos regiones geológicas propias con recursos hipotéticos de cobre de 7,7 Mt y 9,7 Mt (total **17,4 Mt**) — 37,3 Mt es el promedio de otras tres regiones *compartidas* con Ecuador, Perú y Panamá, no un total exclusivo de Colombia (corrección verificada contra la fuente primaria el 14-sep-2026, ver `docs/09-metodologia-pipeline.md`) — y **97% del territorio nacional sigue sin explorar**.
4. **UPME ya recomendó, desde 2023, rehabilitar la Red Férrea del Pacífico** (conexión centro del país–puerto de Buenaventura) como prioridad de infraestructura para el transporte de concentrado de cobre, y sugirió explícitamente buscar cooperación técnica con Chile para la reglamentación de relaves — recomendaciones oficiales que ya existían antes del marco con EE. UU. y que este documento no había recogido.

## 2. Horizonte a 2050: qué dicen las fuentes (y dónde discrepan)

**Actualización 2026-09-14 (Fase 6):** esta sección se reconstruyó con el dataset oficial del IEA Critical Minerals Data Explorer 2026 (Excel descargado con cuenta gratuita — ver `pipeline/phase6_iea/`), que reemplaza las cifras de mercado de segunda mano usadas antes.

| Fuente (oficial IEA 2026) | Escenario | 2025 | 2030 | 2035 | 2040 | 2050 |
|---|---|---|---|---|---|---|
| Demanda total de cobre | Current Policies | 27.775 kt | 30.792 kt | 32.359 kt | 33.580 kt | 35.888 kt |
| Demanda total de cobre | Stated Policies | 27.775 kt | 31.370 kt | 33.522 kt | 34.984 kt | 37.572 kt |
| Demanda total de cobre | High Demand | 27.775 kt | 31.967 kt | 34.294 kt | 35.719 kt | 38.066 kt |
| Oferta minera | "Base case" (minas existentes + en construcción, sin proyectos nuevos) | 23.227 kt | 24.571 kt | 20.733 kt | 17.183 kt | — |
| **Brecha calculada** (Stated Policies − base case) | — | — | **6.799 kt** | **12.789 kt** | **17.801 kt** | — |

**La brecha casi se triplica entre 2030 y 2040** bajo el escenario de política ya declarada por los gobiernos — el argumento cuantitativo más fuerte de todo este repositorio a favor de que el déficit de cobre es estructural. La oferta "base case" del propio IEA **decrece** después de 2030 porque no incluye proyectos aún no aprobados — es, literalmente, la ilustración oficial de cuánta inversión nueva hace falta.

**Sobre la cifra de "70+ Mtpa a 2050" citada en versiones anteriores:** esa cifra provenía de un resumen de prensa sobre S&P Global/Wood Mackenzie que nunca se verificó contra el informe primario de esas firmas. Se conserva en `data/metricas_demanda_global_cobre.json` únicamente como referencia de la divergencia con la fuente oficial (que llega a ~38 Mtpa en el escenario más agresivo del propio IEA, no 70), marcada explícitamente como no verificada.

**Consecuencia práctica para Colombia:** cualquier plan de infraestructura (puertos, fundición, energía) debe dimensionarse contra el escenario Stated Policies del IEA (el punto medio, ya con compromisos climáticos declarados), no contra el escenario de mercado más optimista sin verificar.

## 3. Puntos a favor

1. Marco bilateral EE. UU.–Colombia con financiamiento comprometido y plazo definido (vence marzo de 2027).
2. Déficit estructural global garantiza demanda y precios sostenidos — la brecha entre demanda (Stated Policies) y oferta base case del IEA pasa de 6.799 kt en 2030 a 17.801 kt en 2040 (dataset oficial IEA 2026, ver sección 2).
3. Potencial geológico real y cuantificado (17,4 Mt en dos regiones propias de Colombia, según USGS/UPME) con 97% del territorio sin explorar.
4. El Alacrán probó que obtener la primera licencia ambiental de cobre a gran escala del país es posible (aunque tomó 4+ años).
5. Infraestructura portuaria del Caribe en crecimiento (Barranquilla: 6,7 Mt en el primer semestre de 2026; zonas francas del Atlántico pasaron de 11% a 17% de las exportaciones desde la prepandemia).
6. Ecosistema de centros de datos e IA en expansión en Colombia (mercado de USD 450 M en 2025 a USD 1.440 M proyectados en 2031).
7. Base científica ya construida: mapas metalogénicos y geoquímicos de UPME/SGC, grupos de investigación en la Universidad Nacional y la Universidad de Antioquia.
8. La literatura internacional de IA para mapeo de prospectividad mineral (ver [`02-ia-medicion-y-formulas.md`](02-ia-medicion-y-formulas.md)) ya es aplicable sobre esas bases de datos existentes.

## 4. Puntos en contra / retos

1. **Riesgo geopolítico central:** el proyecto más avanzado del país es 100% de capital chino — contradice el objetivo declarado del marco con EE. UU.
2. Incertidumbre regulatoria activa: Quebradona frenado por la Resolución 855/2025; Soto Norte sin licencia ambiental tras años de intento.
3. Minería ilegal masiva: 85% del oro comercializado es de origen ilegal, 29 de 32 departamentos afectados, +800 bloqueos y +3.600 incursiones no autorizadas contra operaciones legales.
4. Caída reciente y fuerte de la IED minera (-88%) y del PIB minero (-18%): hay que revertir una tendencia negativa, no solo capturar una oportunidad nueva.
5. Tiempos de maduración largos: ~15 años promedio desde el hallazgo hasta la operación.
6. Sin fundición-refinería nacional: se exporta materia prima de bajo valor agregado.
7. Estrés energético ya existente: la reducción del 50% en operaciones de ferroníquel por restricciones de gas anticipa el reto de energizar una futura fundición de cobre.
8. Divergencia de escenarios de demanda (ver sección 2): la planificación no puede apostar a un solo número.
9. **Sismicidad inducida por minería subterránea profunda (nuevo, 14-sep-2026):** Quebradona está diseñada con técnicas de hundimiento de bloques "muy similares" a las de El Teniente (Chile), según el propio informe técnico de UPME. El 31 de julio de 2025, un evento sísmico inducido de magnitud 4,3 Mw en El Teniente causó un colapso que mató a 6 trabajadores — y una investigación de agosto de 2026 confirmó que la cadena de mando **ignoró deliberadamente** las alertas del sistema de monitoreo sísmico y había retirado en 2021 un pilar de seguridad exigido por el diseño aprobado en 2018. No es un riesgo geológico abstracto: es el mismo patrón de Brumadinho (advertencias ignoradas por presión de producción) aplicado a minería subterránea en vez de relaves. Análisis completo, comparación internacional de regulación y propuesta de gemelo digital para Colombia en [`docs/12-sismicidad-inducida-y-gemelo-digital.md`](12-sismicidad-inducida-y-gemelo-digital.md).

## 5. Infraestructura señalada: estado y brechas

| Componente | Estado 2026 | Brecha a cerrar |
|---|---|---|
| Minas y concentradoras | 1 operando, 5+ en distintas fases | Resolver incertidumbre regulatoria de 2-3 proyectos frenados |
| Fundición-refinería | 0 plantas | Estudio de factibilidad + planta piloto (ver KPI en `/data`) |
| Energía | Ya con estrés (ferroníquel -50%) | Priorizar solar de La Guajira para nueva demanda industrial |
| Puertos Caribe | Barranquilla: récord mensual de 1,32 Mt en jul-2026 | Habilitar terminales específicas para concentrado/cátodo |
| Corredores viales/férreos | Existentes pero no dimensionados para nuevo volumen | Estudio de capacidad Antioquia/Cesar/Guajira → Caribe |
| Mapeo de prospectividad con IA | Inexistente como programa formal | Ver `03-estudios-colombia-y-ejecucion.md` |

## 6. Qué hacer y cómo ejecutarlo (resumen — detalle en `03-estudios-colombia-y-ejecucion.md`)

1. Resolver la tensión de origen de capital: exigir diversificación de capital en la ronda de 14 áreas (similar a un filtro tipo CFIUS de EE. UU. para activos estratégicos).
2. Elevar el presupuesto de exploración de USD 90 M a USD 500 M/año mediante cofinanciamiento público-privado apalancado en el marco con EE. UU.
3. Lanzar un programa nacional de mapeo de prospectividad con IA sobre el 97% no explorado, usando los datos ya existentes de UPME/SGC.
4. Estandarizar plantillas de EIA para proyectos de cobre pórfido, para reducir el promedio de 15 años sin bajar el estándar ambiental.
5. Condicionar nuevas licencias a fondos de cierre y garantías financieras independientes desde el primer contrato (ya cubierto en el informe original).

---
*Ver también: [00-README (dashboard)](../README.md) · [Fuentes completas](05-fuentes.md)*
