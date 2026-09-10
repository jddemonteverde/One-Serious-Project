.DEFAULT_GOAL := help

PYTHON ?= python3.12
VENV := .venv
VENV_PYTHON := $(VENV)/bin/python

.PHONY: help
help:
	@printf '%s\n' \
		'One Serious Project' \
		'' \
		'Available commands:' \
		'  make install   Create the local virtual environment and install app dependencies' \
		'  make run       Run the API locally using environment configuration' \
		'' \
		'Override the interpreter with PYTHON=<path>. Additional commands will be' \
		'added as the project evolves.'

$(VENV_PYTHON):
	$(PYTHON) -m venv $(VENV)

.PHONY: install
install: $(VENV_PYTHON)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install --requirement app/requirements.txt

.PHONY: run
run:
	@test -x $(VENV_PYTHON) || { printf '%s\n' 'Virtual environment not found. Run: make install' >&2; exit 1; }
	$(VENV_PYTHON) -m app
