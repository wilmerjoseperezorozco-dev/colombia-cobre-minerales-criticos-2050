# Atajos para instalar, correr y probar el pipeline.
#
# En Windows sin `make` instalado (no viene por defecto), usar directamente
# los comandos de cada target — están listados también en README.md y en
# docs/09-metodologia-pipeline.md, sección "Cómo ejecutarlo".

.PHONY: install install-dev run test validate audit lint clean

install:
	pip install -r pipeline/requirements.txt

install-dev:
	pip install -r pipeline/requirements-dev.txt

run:
	python pipeline/run_pipeline.py

test:
	python -m pytest tests/ -v

validate:
	python pipeline/validaciones/validar_dataset_maestro.py

audit:
	python pipeline/auditoria_semanal/comparar_dataset_maestro.py

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
