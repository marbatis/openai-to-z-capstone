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
