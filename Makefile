.PHONY: help install lint lint-fix fmt test notebook notebook2 kernel venv clean

# Configurable paths and names
VENV ?= .venv
PYTHON ?= $(VENV)/bin/python
JUPYTER ?= $(VENV)/bin/jupyter
KERNEL ?= zexplorer
NOTEBOOK ?= notebooks/01_checkpoint1.ipynb

help:
	@echo "Targets:"
	@echo "  install   - pip install -r requirements.txt"
	@echo "  lint      - ruff check ."
	@echo "  lint-fix  - ruff --fix + black format"
	@echo "  fmt       - black ."
	@echo "  test      - pytest"
	@echo "  kernel    - install ipykernel for venv ($(KERNEL))"
	@echo "  notebook  - launch Jupyter using venv kernel"
	@echo "  notebook2 - open notebooks/02_checkpoint2.ipynb"
	@echo "  venv      - create .venv and install requirements"
	@echo "  clean     - remove .venv and Python caches"

install:
	pip install -r requirements.txt

lint:
	ruff check .

lint-fix:
	ruff check . --fix || true
	black .

fmt:
	black .

test:
	pytest

notebook:
	$(MAKE) venv kernel
	$(JUPYTER) notebook $(NOTEBOOK)

notebook2:
	$(MAKE) NOTEBOOK=notebooks/02_checkpoint2.ipynb notebook

kernel:
	@# Install a named Jupyter kernel backed by the venv's Python
	$(MAKE) venv
	$(PYTHON) -m ipykernel install --user --name $(KERNEL) --display-name "Python ($(KERNEL))"

venv:
	@# Create venv if missing and install requirements
	@if [ ! -x "$(PYTHON)" ]; then \
	  echo "Creating virtualenv at $(VENV)"; \
	  python3 -m venv $(VENV); \
	fi
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -r requirements.txt

clean:
	@echo "Cleaning Python caches and virtualenv..."
	@find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	@find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
	@find . -name '.ipynb_checkpoints' -type d -prune -exec rm -rf {} +
	@rm -rf .pytest_cache .ruff_cache .mypy_cache
	@rm -rf $(VENV)
# ---- Marajó AOI helpers ----
marajo-preview:
	python scripts/aoi_marajo_preview.py

marajo: rat-setup
	jupyter notebook notebooks/10a_ALOS2_MARAJO.ipynb

marajo-gedi: rat-setup
	jupyter notebook notebooks/11a_GEDI_MARAJO.ipynb

marajo-all: rat-setup
	jupyter notebook notebooks/10a_ALOS2_MARAJO.ipynb notebooks/11a_GEDI_MARAJO.ipynb

.PHONY: marajo move-downloads
move-downloads:
	@bash scripts/move_downloads_to_exports.sh

marajo:
	@. .venv/bin/activate && python scripts/run_marajo_pipeline.py --topN 5 --buffer_m 6000

# --- AOI-aware helpers ---
.PHONY: move-downloads
move-downloads:
	@PREFIX=$(PREFIX) bash scripts/move_downloads_to_exports.sh

.PHONY: marajo-pipeline santarem-pipeline tapajos-pipeline
marajo-pipeline:
	@. .venv/bin/activate && python scripts/run_marajo_pipeline.py --prefix marajo --topN 5 --buffer_m 6000

santarem-pipeline:
	@. .venv/bin/activate && python scripts/run_marajo_pipeline.py --prefix santarem --topN 5 --buffer_m 6000

tapajos-pipeline:
	@. .venv/bin/activate && python scripts/run_marajo_pipeline.py --prefix tapajos --topN 5 --buffer_m 6000
