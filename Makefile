.PHONY: help install lint fmt test notebook kernel

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

install:
	pip install -r requirements.txt

lint:
	ruff check .

fmt:
	black .

test:
	pytest

notebook:
	@# Ensure venv python exists
	@if [ ! -x "$(PYTHON)" ]; then \
	  echo "Virtual env not found at $(PYTHON)"; \
	  echo "Create it with: python -m venv $(VENV) && source $(VENV)/bin/activate && pip install -r requirements.txt"; \
	  exit 1; \
	fi
	$(MAKE) kernel
	$(JUPYTER) notebook $(NOTEBOOK)

kernel:
	@# Install a named Jupyter kernel backed by the venv's Python
	@if [ ! -x "$(PYTHON)" ]; then \
	  echo "Virtual env not found at $(PYTHON)"; \
	  echo "Create it with: python -m venv $(VENV) && source $(VENV)/bin/activate && pip install -r requirements.txt"; \
	  exit 1; \
	fi
	$(PYTHON) -m ipykernel install --user --name $(KERNEL) --display-name "Python ($(KERNEL))"

