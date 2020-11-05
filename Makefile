.PHONY: help bootstrap build dist redist install install-from-source clean clean-build clean-tests clean-venv clean-docs uninstall test test37 test38 test39 release upload test-upload docs

.DEFAULT_GOAL := help

RM = rm -rf
TESTOPTIONS = --doctest-modules --cov=cypack
TESTS = src tests
PYTHON ?= python

TOXOPTIONS ?=
TOXINI ?= tox.ini
TOX = tox -c $(TOXINI) $(TOXOPTIONS)

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
    match = re.match(r'^([a-z0-9A-Z_-]+):.*?## (.*)$$', line)
    if match:
        target, help = match.groups()
        print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:  ## Show this help
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

build: bootstrap ## Build extensions
	CYTHONIZE=1 $(TOX) -e run-cmd -- python setup.py build

dist: bootstrap ## builds source and wheel package
	CYTHONIZE=1 $(TOX) -e run-cmd -- python setup.py sdist
	CYTHONIZE=1 $(TOX) -e run-cmd -- python setup.py bdist_wheel
	ls -l dist

dist-check: dist ## Check all dist files for correctness
	$(TOX) -e run-cmd -- twine check dist/*

redist: clean dist

release: bootstrap ## Create a new version, package and upload it
	python3.8 -m venv .venv/release
	.venv/release/bin/python -m pip install click gitpython pytest
	.venv/release/bin/python ./scripts/release.py

test-upload: bootstrap clean-build dist ## package and Upload a release to test.pypi.org
	$(TOX) -e run-cmd -- twine check dist/*
	$(TOX) -e run-cmd -- twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload: bootstrap clean-build dist ## package and upload a release to pypi.org
	# $(TOX) -e run-cmd -- twine check dist/*
	# $(TOX) -e run-cmd -- twine upload dist/*
	make test-upload

install:  ## Install the package into the system $(PYTHON)
	CYTHONIZE=1 $(PYTHON) -m pip install .

install-from-sdist: dist  ## Install the package from the source distribution into the system $(PYTHON)
	$(PYTHON) -m pip install -v dist/mg-cython-package-example-*.tar.gz

install-from-wheel: dist  ## Install the package from the wheel distribution into the system $(PYTHON)
	$(PYTHON) -m pip install -v dist/mg_cython_package_example-*.whl

uninstall:  ## Uninstall the package from the system $(PYTHON)
	$(PYTHON) -m pip uninstall cython-package-example

clean: ## remove all build, docs, test, and coverage artifacts, as well as tox environments
	python scripts/clean.py all

clean-build: ## remove build artifacts
	python scripts/clean.py build

clean-tests: ## remove test and coverage artifacts
	python scripts/clean.py tests

clean-venv: ## remove tox virtual environments
	python scripts/clean.py venv

docs: bootstrap ## generate Sphinx HTML documentation, including API docs
	$(TOX) -e docs
	@echo "open docs/_build/html/index.html"

clean-docs: ## remove documentation artifacts
	python scripts/clean.py docs

bootstrap: ## verify that tox is available
	python scripts/bootstrap.py

test: bootstrap ## run tests for all supported Python versions
	$(TOX) -e py37-test -- $(TESTS)
	$(TOX) -e py38-test -- $(TESTS)

test37: bootstrap ## run tests for Python 3.7
	$(TOX) -e py37-test -- $(TESTS)

test38: bootstrap ## run tests for Python 3.8
	$(TOX) -e py38-test -- $(TESTS)

test39: bootstrap ## run tests for Python 3.9
	$(TOX) -e py39-test -- $(TESTS)
