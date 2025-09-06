
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
\t@# Ensure venv python exists
\t@if [ ! -x "$(PYTHON)" ]; then \\
\t  echo "Virtual env not found at $(PYTHON)"; \\
\t  echo "Create it with: python -m venv $(VENV) && source $(VENV)/bin/activate && pip install -r requirements.txt"; \\
\t  exit 1; \\
\tfi
\t$(MAKE) kernel
\t$(JUPYTER) notebook $(NOTEBOOK)

kernel:
\t@# Install a named Jupyter kernel backed by the venv's Python
\t@if [ ! -x "$(PYTHON)" ]; then \\
\t  echo "Virtual env not found at $(PYTHON)"; \\
\t  echo "Create it with: python -m venv $(VENV) && source $(VENV)/bin/activate && pip install -r requirements.txt"; \\
\t  exit 1; \\
\tfi
\t$(PYTHON) -m ipykernel install --user --name $(KERNEL) --display-name "Python ($(KERNEL))"
