# Project-specific constants
NAME=hostedpi
DOC_HTML=docs/build/html
DOC_TREES=docs/build/doctrees
DOC_REQS=rtd_requirements.txt

# Default target
all:
	@echo "make install - Install on local system"
	@echo "make develop - Install symlinks for development"
	@echo "make format - Format all Python code with isort and black"
	@echo "make test - Run tests"
	@echo "make clean - Remove all generated files"
	@echo "make build - Build the package release files"
	@echo "make release - Release to PyPI"
	@echo "make doc - Build the docs as HTML"
	@echo "make doc-serve - Serve the docs locally"

install:
	pip install .

develop:
	pip install -U pip
	pip install -U setuptools
	pip install -U wheel
	pip install -U "poetry>2"
	poetry install --with dev --all-extras
	hostedpi --install-completion

format:
	isort .
	black .

test:
	pytest

clean:
	rm -rf dist

build: clean
	poetry build

release: build
	twine upload dist/*

doc:
	rm -rf docs/build/
	sphinx-build -b html -d $(DOC_TREES) docs/ $(DOC_HTML)

doc-serve:
	python -m http.server -d $(DOC_HTML)

doc-reqs:
	echo "." > $(DOC_REQS)
	pip freeze | grep -i sphinx >> $(DOC_REQS)
	pip freeze | grep -i autodoc >> $(DOC_REQS)

.PHONY: all install develop format test clean build release doc doc-serve doc-reqs