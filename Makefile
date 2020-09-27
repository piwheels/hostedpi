# vim: set noet sw=4 ts=4 fileencoding=utf-8:

# Project-specific constants
DOC_HTML=docs/build/html
DOC_TREES=docs/build/doctrees

# Default target
all:
	@echo "make install - Install on local system"
	@echo "make develop - Install symlinks for development"
	@echo "make test - Run tests"
	@echo "make doc - Build the docs as HTML"
	@echo "make doc-serve - Serve the docs"

install:
	pip install .

develop:
	pip install -e .

test:
	coverage run --rcfile coverage.cfg -m pytest -v tests
	coverage report --rcfile coverage.cfg

doc:
	sphinx-build -b html -d $(DOC_TREES) docs/ $(DOC_HTML)

doc-serve:
	cd $(DOC_HTML) && python -m http.server
