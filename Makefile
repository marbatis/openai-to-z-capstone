
.PHONY: help install lint fmt test notebook

help:
	@echo "Targets:"
	@echo "  install   - pip install -r requirements.txt"
	@echo "  lint      - ruff check ."
	@echo "  fmt       - black ."
	@echo "  test      - pytest"
	@echo "  notebook  - launch Jupyter Notebook"

install:
	pip install -r requirements.txt

lint:
	ruff check .

fmt:
	black .

test:
	pytest

notebook:
	jupyter notebook
