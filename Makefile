.PHONY: help install lint fmt test notebook kernel venv

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
	@echo "  fmt       - black ."
	@echo "  test      - pytest"
	@echo "  kernel    - install ipykernel for venv ($(KERNEL))"
	@echo "  notebook  - launch Jupyter using venv kernel"
	@echo "  venv      - create .venv and install requirements"

install:
	pip install -r requirements.txt

lint:
	ruff check .

fmt:
	black .

test:
	pytest

notebook:
	$(MAKE) venv kernel
	$(JUPYTER) notebook $(NOTEBOOK)

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
