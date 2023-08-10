SHELL:=/usr/bin/env bash -O globstar

# CI/CD
clean:
	rm -rf .mypy_cache
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

mypy:
	python -m mypy .

black:
	 python -m black ./

isort:
	python -m isort .

fix: isort black

flake8:
	python -m flake8

black-check:
	 python -m black --check --diff ./

lint: flake8 black-check mypy

fix-lint: clean fix lint

start:
	python -m strawberry server strawberry_sandbox.schema

