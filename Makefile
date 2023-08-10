SHELL:=/usr/bin/env bash -O globstar

# CI/CD
clean:
	cd getway && make clean
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf test-results
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

fix:
	cd getway && make fix

lint:
	cd getway && make lint

fix-lint:
	cd getway && make fix-lint

test:
	cd getway && make test

start-getway:
	cd getway && make start
