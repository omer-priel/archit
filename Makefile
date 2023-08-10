SHELL:=/usr/bin/env bash -O globstar

# CI/CD
clean:
	cd gateway && make clean
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf test-results
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

fix:
	cd gateway && make fix

lint:
	cd gateway && make lint

fix-lint:
	cd gateway && make fix-lint

test:
	cd gateway && make test

start-gateway:
	cd gateway && make start
