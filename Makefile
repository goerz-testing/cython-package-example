.PHONY: build dist redist install install-from-source clean uninstall test test38

TESTENV =
RM = rm
TESTOPTIONS = --doctest-modules --cov=cypack
TESTS = src tests

build:
	CYTHONIZE=1 ./setup.py build

dist:
	CYTHONIZE=1 ./setup.py sdist bdist_wheel

redist: clean dist

install:
	CYTHONIZE=1 pip install .

install-from-source: dist
	pip install dist/cython-package-example-0.1.5.tar.gz

clean:
	$(RM) -rf build dist src/*.egg-info
	$(RM) -rf src/cypack/{utils.c,answer.c,fibonacci.c} src/cypack/sub/wrong.c
	$(RM) -rf .pytest_cache
	$(RM) -rf .venv
	find . -name __pycache__ -exec rm -r {} +
	#git clean -fdX

uninstall:
	pip uninstall cython-package-example

.venv/py38/bin/py.test:
	python3.8 -m venv .venv/py38
	.venv/py38/bin/python -m pip install cython
	CYTHONIZE=1 .venv/py38/bin/python -m pip install -e .[dev,docs]

test38: .venv/py38/bin/py.test ## run tests for Python 3.8
	$(TESTENV) $< -v $(TESTOPTIONS) $(TESTS)

test: test38
