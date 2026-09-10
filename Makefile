.DEFAULT_GOAL := help

# The repository can hold several applications under app/. APP selects which one
# the commands below act on; PACKAGE is its importable Python package name.
APP     ?= habit-tracker
PYTHON  ?= python3.12

BACKEND := app/$(APP)/backend
PACKAGE := $(subst -,_,$(APP))
VENV    := $(BACKEND)/.venv
VENV_PYTHON := $(VENV)/bin/python

.PHONY: help
help:
	@printf '%s\n' \
		'One Serious Project' \
		'' \
		'Available commands:' \
		'  make install   Create the application virtual environment and install backend dependencies' \
		'  make run       Run the backend locally using environment configuration' \
		'' \
		'Select an application with APP=<name> (default: habit-tracker) and override' \
		'the interpreter with PYTHON=<path>. Additional commands will be added as the' \
		'project evolves.'

$(VENV_PYTHON):
	$(PYTHON) -m venv $(VENV)

.PHONY: install
install: $(VENV_PYTHON)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install --requirement $(BACKEND)/requirements.txt

.PHONY: run
run:
	@test -x $(VENV_PYTHON) || { printf '%s\n' 'Virtual environment not found. Run: make install' >&2; exit 1; }
	cd $(BACKEND) && .venv/bin/python -m $(PACKAGE)
