#ROOT := $(dir $(lastword $(MAKEFILE_LIST)))
ROOT := $(shell pwd)

.PHONY: coverage docs mypy test publish-to-pypi tox
.PHONY: ruff-check ruff-fix ruff-format rstcheck

coverage:
	coverage run -m pytest tests
	coverage report -m

docs:
	cd "$(ROOT)"/docs && make clean && make html

mypy:
	MYPYPATH=src mypy --namespace-packages --explicit-package-bases --strict src tests

ruff-check:
	ruff check src tests docs

ruff-fix:
	ruff fix src tests docs

ruff-format:
	ruff format src tests docs

rstcheck:
	rstcheck -r docs/

publish-to-pypi:
	poetry publish --build

test:
	pytest tests/

tox:
	tox
