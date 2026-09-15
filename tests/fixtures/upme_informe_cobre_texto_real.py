"""
Fixture: texto REAL extraído con pdfplumber del "Informe Cobre" de la
Subdirección de Minería de UPME, capturado el 14-sep-2026 al construir la
Fase 7. Cada bloque corresponde a las páginas exactas donde se encontró
cada tabla (ver pipeline/phase7_upme_sgc/fetch_upme_informe_cobre.py).
"""

TABLA_1_POTENCIAL_NACIONAL = """Tabla 1. Estimación de recursos en zonas con influencia en Colombia
Recursos Hipotéticos y/o Especulativos
Promedio de Probabilidad Promedio de Probabilidad
Recursos de Recursos Recursos de Recursos
Nombre Región Geológica Estimados In- In-situ(%) Estimados económicos
situ (Millones Económicos (%)
de toneladas) (Millones de
Toneladas)
Plate 22, Porphyry Copper Assessment for Tract
39 2 21 10
005pCu1005 Miocene Chaucha-Colombia and Ecuardor
Plate 23, Porphyry Copper Assessment for Tract
005pCu1003, Jurassic San 40 2 20 15
Carlos-Colombia, Ecuardor and Peru
Plate 24, Porphyry Copper Assessment for Tract
33 3 18 14
005pCu1001, Paleocene-Eocene Acandi-Colombia, Ecuardor and Panama
Plate 25, Porphyry Copper Assessment for Tract
7.7 6 4.4 58
005pCu1004, Cretaceous Infierno- Chili- Colombia
Plate 26, Porphyry Copper Assessment for Tract
005pCu1002, Jurassic California- 9.7 7 5.2 55
Colombia and Venezuela
Fuente: USGS Assessment of Undiscovered Copper Resources of the World, 2015, Scientific
Investigations Report 2018–5160 Version 1.1, May 24, 2019.
"""

TABLA_2_EL_ROBLE = """Tabla 2. Recursos proyecto el Roble (a 30 de septiembre de 2020)
TENORES CANTIDAD DE METAL
CATEGORIA MENA (t)
%Cu (g/t) Au Cu (Lb) (oz) Au
Recursos
1,039,200 4.34 2.29 75,745,700 76,500
Medidos
Recursos
135,200 4.06 2.62 8,597,700 11,400
Indicados
Medidos
1,174,400 4.30 2.33 84,343,400 87,900
+Indicados
Recursos
17,100 2.03 3.41 186,400 1,900
Inferidos
Fuente: http://aticomining.com/_resources/technical-reports/ATICO-TECHNICAL-REPORT-
MINER-2021.pdf.
2.2.2. Proyecto Quebradona: el resto del texto no es relevante para este fixture.
"""

TEXTO_TEXTO_LIBRE_POTENCIAL_COLOMBIA = """
Las filas 1, 2 y 3 de la tabla 1, corresponden a información que abarca Ecuador, Perú,
Colombia y Panamá y en promedio en dichas áreas estiman recursos hipotéticos de mineral de
cobre de 37.3 millones de toneladas, mientras que las filas 4 y 5 corresponde a áreas que
están ubicadas en Colombia y se estima un potencial 7.7 y 9.7 millones de toneladas de
recursos hipotéticos, respectivamente.
"""
