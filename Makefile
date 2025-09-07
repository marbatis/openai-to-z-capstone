.PHONY: help install lint lint-fix fmt test notebook notebook2 kernel venv clean marajo-fig

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
	@echo "  marajo-fig - build Marajó PNG/PDF figure from exports"

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

marajo-fig:
	$(MAKE) venv
	@# Install minimal extras for figure generation
	$(PYTHON) -m pip install -q numpy pillow tifffile scikit-image matplotlib
	@# Ensure dirs
	mkdir -p data/exports figures
	@# Try to copy from Google Drive (Drive for Desktop) if present
	EE_GLOB="$(HOME)/Library/CloudStorage/GoogleDrive*/My Drive/EarthEngine"; \
	EE_DIR=$$(ls -d $$EE_GLOB 2>/dev/null | head -n1 || true); \
	if [ -n "$$EE_DIR" ] && [ -d "$$EE_DIR" ]; then \
	  echo "Found EarthEngine folder at: $$EE_DIR"; \
	  cp -vn "$$EE_DIR"/marajo_*_delta_*.tif data/exports/ || true; \
	else \
	  echo "Could not find a local Google Drive 'EarthEngine' folder."; \
	  echo "If you don't use Drive for Desktop, download these four to data/exports/:"; \
	  echo "  marajo_ALOS2_delta_db.tif, marajo_ALOS2_delta_rgb.tif,"; \
	  echo "  marajo_S1VV_delta_db.tif,  marajo_S1VV_delta_rgb.tif"; \
	fi
	@# Build figure (PNG + PDF)
	$(PYTHON) scripts/make_marajo_figure.py --in-dir data/exports --out-dir figures
	@# Open PNG on macOS if available
	@if command -v open >/dev/null 2>&1; then open figures/marajo_delta_overview.png || true; fi
# ---- Marajó AOI helpers ----
marajo-preview:
	python scripts/aoi_marajo_preview.py

marajo: rat-setup
	jupyter notebook notebooks/10a_ALOS2_MARAJO.ipynb

marajo-gedi: rat-setup
	jupyter notebook notebooks/11a_GEDI_MARAJO.ipynb

marajo-all: rat-setup
	jupyter notebook notebooks/10a_ALOS2_MARAJO.ipynb notebooks/11a_GEDI_MARAJO.ipynb
