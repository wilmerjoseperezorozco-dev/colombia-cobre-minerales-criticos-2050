# Diseño del piloto de prospectividad mineral con IA (issue #9): de la idea general a un plan ejecutable

> Hasta el 25-sep-2026, el issue #9 ("Piloto de mapeo de prospectividad mineral con IA") existía como intención sin metodología concreta. Li et al. (2026, *Chemical Geology*, [10.1016/j.chemgeo.2026.123659](https://doi.org/10.1016/j.chemgeo.2026.123659)) — incorporado el mismo día a `docs/05` — publica un método específico, con desempeño medido, aplicable directamente a los datos que Colombia ya tiene. Este documento traduce ese método en un plan de piloto real.

## 1. El método publicado, en términos operativos

Li et al. entrenaron un modelo de machine learning interpretable para clasificar el **tipo genético** de un yacimiento (magmático, hidrotermal, sedimentario — incluye pórfido cuprífero) a partir de la **composición de elementos traza en calcopirita**, el mineral de cobre más común de la corteza terrestre. Con un set de datos de 5.232 análisis de 232 depósitos mundiales, el modelo alcanzó 0,96 de exactitud balanceada, y el análisis de atribución de características identificó qué elementos traza son diagnósticos de cada tipo genético — es decir, el modelo no es una caja negra, explica *por qué* clasifica un depósito de una forma u otra.

**Por qué esto es aplicable a Colombia hoy, no en un horizonte de años:** no requiere sensores remotos nuevos, no requiere sobrevuelos, no requiere esperar a que se apruebe presupuesto para un satélite propio. Requiere análisis de **química mineral de muestras que ya existen o son baratas de tomar** — es el tipo de dato que un laboratorio de geoquímica universitario colombiano (Universidad Nacional, Universidad de Antioquia, ambas ya citadas en `docs/05`) puede generar.

## 2. Plan de piloto en 4 fases

### Fase 1 — Compilación de muestras de referencia (bajo costo, ejecutable ya)
Recolectar y/o solicitar acceso a análisis de calcopirita de los proyectos colombianos ya identificados en este repositorio, donde la clasificación genética ya se conoce por otras vías (para poder validar el modelo contra la verdad conocida antes de aplicarlo a lo desconocido):

| Proyecto | Departamento | Estado | Por qué sirve como caso de validación |
|---|---|---|---|
| El Roble | Chocó | En producción | Único yacimiento con décadas de datos de explotación — la mejor referencia de "verdad conocida" del país |
| El Alacrán | Córdoba | Licencia ambiental completa | Caracterización geológica ya avanzada por el operador (JCHX) |
| Quebradona | Antioquia | Exploración prorrogada | Pórfido cuprífero clásico, bien caracterizado por AngloGold Ashanti |
| Soto Norte | Santander | Detenido | Datos de exploración histórica ya existentes (Eco Oro / Aris Mining) |
| Mocoa (Libero Cooper) | Putumayo | Exploración | Menos caracterizado — buen candidato para *probar* el modelo, no solo validarlo |

### Fase 2 — Aplicación del modelo publicado (o reentrenamiento con datos propios)
Dos rutas posibles, en orden de preferencia por costo/rapidez:
1. **Contactar a los autores** (Li, Cao, Qin et al., Universidad Tecnológica de Mongolia Interior / Academia China de Ciencias) para preguntar si el modelo entrenado o el código están disponibles — es la ruta más rápida si el paper lo permite (revisar la sección de disponibilidad de datos del artículo, no asumida aquí).
2. **Reentrenar el mismo enfoque metodológico** (transformación de datos, balanceo de clases, el mismo tipo de algoritmo interpretable) sobre el dataset colombiano compilado en la Fase 1 — más lento pero no depende de la cooperación de terceros.

### Fase 3 — Extensión al 97% sin explorar (el objetivo real del pipeline)
Una vez validado contra los 5 proyectos conocidos, aplicar el modelo a análisis de calcopirita de zonas del cinturón cuprífero colombiano sin caracterizar — empezando por las áreas de la Ronda ANM de 14 Áreas Estratégicas (Antioquia, La Guajira, Cesar, Tolima) y la zona de El Infierno-Chili en Tolima (issue #15, ya georreferenciado con precisión esta misma semana).

### Fase 4 — Integración al pipeline de datos de este repositorio
Si el piloto produce resultados útiles, el siguiente paso natural es una Fase 10 del pipeline ejecutable (`pipeline/phase10_prospectividad_ia/`), siguiendo el mismo patrón ya establecido: función pura de clasificación separada de la función de I/O, tests contra fixtures reales, y salida documentada con su nivel de confiabilidad (`estimacion_propia_razonada`, no `curado_investigacion_humana` — un resultado de modelo no es un hecho verificado).

## 3. Qué NO promete este plan (límite honesto)

- El modelo de Li et al. clasifica **tipo genético**, no tonelaje ni ley de mineral — no reemplaza la exploración de campo, la reduce en alcance (dónde priorizar taladros, no cuánto cobre hay).
- Ninguna muestra colombiana fue parte del set de entrenamiento original de 232 depósitos — el desempeño de 0,96 de exactitud balanceada es sobre el dataset mundial, no una garantía de que se replique igual en geología andina sin recalibración.
- Este documento es un diseño de piloto, no el piloto ejecutado. El issue #9 permanece abierto hasta que exista un resultado real, verificado contra al menos uno de los 5 casos de validación de la Fase 1.

---
*Ver también: [IA, medición y fórmulas](02-ia-medicion-y-formulas.md) · [Geografía de sitios candidatos](11-geografia-sitios-candidatos.md) · [Fuentes y estrategia de búsqueda](05-fuentes.md)*
