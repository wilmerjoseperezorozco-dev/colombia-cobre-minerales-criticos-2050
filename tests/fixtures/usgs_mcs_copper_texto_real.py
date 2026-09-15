"""
Fixture: texto REAL extraído con pdfplumber del PDF oficial del USGS
(Mineral Commodity Summaries, edición de febrero de 2026, ficha de Copper),
capturado el 14-sep-2026 al construir la Fase 5. No es texto sintético —
es la salida real de `pdfplumber` sobre el PDF oficial, con sus saltos de
línea y espaciado tal cual, incluyendo el bug real de marcador de nota al
pie pegado al valor de reservas de Australia ("7100,000") que motivó el
guardrail `_corregir_marcadores_de_nota_al_pie` en
`pipeline/phase5_usgs/fetch_usgs_copper_mcs.py`.

Si el USGS cambia el formato de una edición futura, este fixture NO lo
detecta (sigue siendo la edición de 2026) — para eso está la Fase 5
corriendo de verdad en el workflow semanal de GitHub Actions. Lo que este
fixture SÍ detecta es una regresión introducida en el código de parseo.
"""

PAGINA_1 = """COPPER
(Data in thousand metric tons, copper content, unless otherwise specified)
Domestic Production and Use: In 2025, the recoverable copper content of U.S. mine production was an estimated
1.0 million tons, a decrease of 5% from that in 2024, and was valued at an estimated $11 billion, 10% greater than
$10.0 billion in 2024. Arizona was the leading copper-producing State and accounted for approximately 70% of
domestic output; copper was also mined in Alaska, Michigan, Missouri, Montana, Nevada, New Mexico, and Utah.
Salient Statistics—United States: 2021 2022 2023 2024 2025e
Production:
Mine, recoverable 1,230 1,230 1,130 1,050 1,000
Refinery:
Primary (from ore) 931 917 843 882 790
Secondary (from scrap) 49 40 39 39 60
Imports for consumption:
Ore and concentrate 11 12 3 (2) (2)
Refined 919 732 771 903 1,700
Exports:
Ore and concentrate 344 351 339 326 340
Refined 48 27 29 72 110
Consumption:
Reported, refined copper 1,750 1,720 1,580 1,580 1,700
Price, annual average, cents per pound:
U.S. producer, cathode (COMEX + premium) 432.3 410.8 395.3 431.8 490
COMEX, high-grade, first position 424.3 400.7 385.7 421.6 480
"""

PAGINA_2 = """COPPER
Events, Trends, and Issues: In 2025, production of copper was affected by concentrator shutdowns and lower ore
grades at multiple mines in the United States. The COMEX copper price was projected to average a record high of $4.80 per pound in 2025, 14% greater than
$4.22 per pound in 2024. Analysts attributed the increase primarily to uncertainty regarding the implementation of
tariffs on U.S. imports of copper materials.
On November 7, 2025, the U.S. Final 2025 List of Critical Minerals was published in the Federal Register (90 FR 50494).
The changes in the 2025 list from the prior list published in 2022 (87 FR 10381) were the addition of copper, lead,
potash, rhenium, silicon, and silver, based on the U.S. Geological Survey (USGS) updated methodology for the 2025
list.
World Mine and Refinery Production and Reserves: Reserves for Canada, Chile, Peru, Poland, and “Other
countries” were revised based on company, Government, and industry association reports.
Mine production Refinery production Reserves6
2024 2025e 2024 2025e
United States 1,050 1,000 921 850 47,000
Australia 765 730 434 460 7100,000
Canada 515 500 324 320 7,000
Chile 5,510 5,300 1,940 1,700 180,000
China 1,840 1,800 12,400 14,000 41,000
Congo (Kinshasa) 2,990 3,200 2,560 2,800 80,000
Germany — — 597 610 —
India 27 23 545 620 2,200
Indonesia 1,010 710 349 400 21,000
Japan — — 1,570 1,400 —
Kazakhstan 724 710 498 500 20,000
Korea, Republic of — — 604 610 —
Mexico 717 690 489 480 53,000
Peru 2,740 2,700 385 340 85,000
Poland 400 410 589 560 33,000
Russia 1,020 1,300 896 950 80,000
Zambia 823 940 189 270 21,000
Other countries 2,850 3,000 2,310 2,100 210,000
World total (rounded) 23,000 23,000 27,600 29,000 980,000
World Resources:6 The most recent USGS assessment of global copper resources indicated that, as of 2015,
identified resources contained 1.5 billion tons of unextracted copper (2.1 billion tons when past production of 600
million tons is included) and undiscovered resources contained an estimated 3.5 billion tons of copper.8
U.S. Geological Survey, Mineral Commodity Summaries, February 2026
"""

TEXTO_COMPLETO = PAGINA_1 + "\n" + PAGINA_2
