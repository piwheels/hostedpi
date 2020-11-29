# vim: set noet sw=4 ts=4 fileencoding=utf-8:

# Project-specific constants
NAME=hostedpi
DOC_HTML=docs/build/html
DOC_TREES=docs/build/doctrees

# Default target
all:
	@echo "make install - Install on local system"
	@echo "make develop - Install symlinks for development"
	@echo "make build - Build sdist and bdist_wheel"
	@echo "make clean - Remove all generated files"
	@echo "make lint - Run linter"
	@echo "make test - Run tests"
	@echo "make doc - Build the docs as HTML"
	@echo "make doc-serve - Serve the docs locally"
	@echo "make release - Release to PyPI"

install:
	pip install .

develop:
	pip install -U pip
	pip install twine
	pip install -e .[test,doc]

clean:
	rm -rf build/ dist/ $(NAME).egg-info/ docs/build/ .pytest_cache/ .coverage

build: clean
	python setup.py sdist bdist_wheel

lint:
	pylint -E $(NAME)

test: lint
	coverage run --rcfile coverage.cfg -m pytest -v tests
	coverage report --rcfile coverage.cfg

doc:
	rm -rf docs/build/
	sphinx-build -b html -d $(DOC_TREES) docs/ $(DOC_HTML)

doc-serve:
	cd $(DOC_HTML) && python -m http.server

release: build
	twine upload dist/*

.PHONY: all install develop build clean lint test doc doc-serve release
