SHELL := /usr/bin/env bash

PROJECT_ROOT := $(CURDIR)
VENV_DIR := $(PROJECT_ROOT)/venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
RUFF := $(VENV_DIR)/bin/ruff
BLACK := $(VENV_DIR)/bin/black
MYPY := $(VENV_DIR)/bin/mypy
PYTEST := $(VENV_DIR)/bin/pytest

.PHONY: bootstrap lint format typecheck test

bootstrap:
	@echo "Bootstrapping development environment..."
	./scripts/dev_environment_bootstrap.sh

lint:
	@echo "Running ruff..."
	$(RUFF) check .

format:
	@echo "Formatting code with black..."
	$(BLACK) .

typecheck:
	@echo "Running mypy..."
	$(MYPY) .

test:
	@echo "Running pytest..."
	$(PYTEST)
