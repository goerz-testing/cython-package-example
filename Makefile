.PHONY: build dist redist install install-from-source clean uninstall test test38

.DEFAULT_GOAL := help

TESTENV =
RM = rm
TESTOPTIONS = --doctest-modules --cov=cypack
TESTS = src tests
VENV_PYTHON = .venv/py38/bin/python
PYTHON ?= python


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

build: .venv/py38/bin/py.test  ## Build extensions
	CYTHONIZE=1 $(VENV_PYTHON) setup.py build

dist: .venv/py38/bin/py.test  ## Create distribution packages
	CYTHONIZE=1 $(VENV_PYTHON) setup.py sdist bdist_wheel

redist: clean dist

install:  ## Install the package into the system $(PYTHON)
	CYTHONIZE=1 $(PYTHON) -m pip install .

install-from-source: dist  ## Install the package from the source distribution into the system $(PYTHON)
	$(PYTHON) -m pip install dist/cython-package-example-0.1.5.tar.gz

clean:  ## Clean up compilation/distribution files
	$(RM) -rf build dist src/*.egg-info
	$(RM) -rf src/cypack/{utils.c,answer.c,fibonacci.c} src/cypack/sub/wrong.c
	$(RM) -rf .pytest_cache
	$(RM) -rf .venv
	find . -name __pycache__ -exec rm -r {} +
	find src -name '*.so' -exec rm -r {} +

uninstall:  ## Uninstall the package from the systgem $(PYTHON)
	$(PYTHON) -m pip uninstall cython-package-example

.venv/py38/bin/py.test:
	python3.8 -m venv .venv/py38
	CYTHONIZE=1 $(VENV_PYTHON) -m pip install -e .[dev,docs]

test38: .venv/py38/bin/py.test ## Run tests for Python 3.8
	$(TESTENV) $< -v $(TESTOPTIONS) $(TESTS)

test: test38  ## Run all tests
