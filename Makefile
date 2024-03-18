#ROOT := $(dir $(lastword $(MAKEFILE_LIST)))
ROOT := $(shell pwd)

.PHONY: coverage docs mypy test publish-to-pypi tox
.PHONY: ruff-check ruff-fix ruff-format

coverage:
	coverage run -m pytest tests
	coverage report -m

docs:
	cd "$(ROOT)"/docs && make clean && make html

mypy:
	MYPYPATH=src mypy --namespace-packages --explicit-package-bases --strict src tests

ruff-check:
	ruff check src tests

ruff-fix:
	ruff fix src tests

ruff-format:
	ruff format src tests

publish-to-pypi:
	poetry publish --build

test:
	pytest tests/

tox:
	tox
