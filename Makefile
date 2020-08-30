# vim: set noet sw=4 ts=4 fileencoding=utf-8:

# Default target
all:
	@echo "make install - Install on local system"
	@echo "make develop - Install symlinks for development"

install:
	pip install .

develop:
	pip install -e .
