SHELL:=/usr/bin/env bash -O globstar

# environment dependencies
load-env:
	$(eval include .env)
	$(eval export $(shell sed 's/=.*//' .env))

# CI/CD
clean:
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf test-results
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

test: load-env clean
	pytest ./tests --junit-xml=test-results/pytest/results.xml

start: load-env
	python -m uvicorn src.main:app --host=${GETWAY_HOST} --port=${GETWAY_PORT} --reload
