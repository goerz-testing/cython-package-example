# Packaging and Testing of Cython Packages

Testing should be done with `tox`, with a thin `Makefile` wrapper.

Requirements:

* Testing should be "isolated", testing the *installation* of a package
* A `make test`/`tox` call should automatically pick up on changes in the `src` directory ("editable installs")

## Background: Pure Python Packages

### Testing environment (via tox)


The virtual test environments are set up in a `tox.ini` file. For example:

~~~
[testenv]
basepython =
    py39: python3.9
    py38,run,docs,coverage,bootstrap: python3.8
envdir =
    py39: {toxworkdir}/py39
    py38,run,docs,coverage: {toxworkdir}/py38
deps =
    cython
    numpy
    scipy
usedevelop = true
extras=
    dev
passenv = HOME CI TRAVIS TRAVIS_* COVERALLS* CODECOV* SPELLCHECK SSH_AUTH_SOCK http_proxy https_proxy no_proxy
description =
    py{38,39}-test: Run tests in the corresponding environment
    py{38,39}-runcmd: Run arbitrary command following "--" in the corresponding environment
commands_pre =
    python -V
commands =
    py{38,39}-runcmd: {posargs:python -c 'print("No command")'}
    py{38,39}-test: py.test -vvv --doctest-modules --cov=qalgebra --nbval --sanitize-with docs/sources/nbval_sanitize.cfg {posargs:--durations=10 -x -s src tests docs/sources README.rst}
~~~

In the above example, `cython`, `numpy`, and `scipy` (the "build-dependencies" that `setup.py` depends on) are installed first, all other dependencies and the package itself are installed by `tox` running

~~~
pip install -e .
~~~

This is due to `usedevelop = true`, a.k.a [setuptools "Development Mode"](https://setuptools.readthedocs.io/en/latest/userguide/development_mode.html).


### Packaging

For packaging, the `Makefile` invokes the `setup.py` to generate distributions in the `dist` sub-directory. For example:

~~~
TOXOPTIONS ?=
TOXINI ?= tox.ini
TOX = tox -c $(TOXINI) $(TOXOPTIONS)

dist: bootstrap ## builds source and wheel package
	$(TOX) -e run-cmd -- python setup.py sdist
	$(TOX) -e run-cmd -- python setup.py bdist_wheel
	ls -l dist
~~~

This relies on the following setup in `tox.ini`:

~~~
[testenv:run-cmd]
description = Run arbitrary command following "--" in the current stable environment, e.g. "tox -e run-cmd -- ipython"
commands = {posargs:python -c 'print("No command")'}
~~~

It creates a source distribution (`.tar.gz` file) and a compiled "wheel" (`.whl` file), see [Packaging your project](https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project) for details.

The source distribution is an archive that contains the files specified in [`MANIFEST.in`](https://packaging.python.org/guides/using-manifest-in/) in addition to a set of "standard files" and some meta-data. It must contain all the files required to install the package on *any* platform. It may also contain tests and documentation.

The wheel is a zip file containing data directly to be un-packed into the Python installation's `site-packages` directory (plus some metadata). See [What Are Python Wheels and Why Should You Care?](https://realpython.com/python-wheels/) and [PEP 427](https://www.python.org/dev/peps/pep-0427/) for a detailed overview.


## Traditional Cython Packages

A package that contains extension modules in Cython sets up "cythonization" and compilations in the `setup.py` file. This is described in the [Cython documentation](https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html). Essentially:

* Set up a list of `setuptools.Extension` instances, one for each `pyx` file.
* Run this list through the `Cython.Build.cythonize` function. This translates the `.pyx` files into `.c` files and transforms the `Extension` instances such that they use that `c` file in their `sources` attribute.

### Testing and development installs

Since we are testing with editable installs (see above), any changes in Python files are automatically picked up by the tests. For `.pyx` files, this is not true automatically. We have to make sure that `python setup.py build_ext --inplace --verbose` is called to both update the `.c` files from any changed `.pyx` files, and then compile them into `.so` files. You may put this command into the `commands_pre` entry of the `[testenv]` section in [`tox.ini`](https://github.com/goerz-testing/cython-package-example/blob/master/tox.ini).


### Package installations

The `setup.py` file included in the source distribution is run by `pip` anytime the package is installed from the Python package index. While for testing and *creating* distributions it's no problem if the `setup.py` file depends on Cython, as it is always executed by the python from the (tox) virtual environment over which we have full control. On the other hand, when *installing* the source distribution the `setup.py` script is run by whatever Python is executing `pip`, and we have no control over whether that Python has Cython (or any other package that `setup.py` may depend on) installed at all or in any specific version.

The traditional response to this has been to include in the source distribution the `.c` files that Cython generates. Then, the `setup.py` file can be written such that it depends only optionally on Cython. The [Cython documentation has specific instructions for this](https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules). Basically, one can put a `no_cythonize` function into `setup.py`:

~~~python
def no_cythonize(extensions, **_ignore):
    """Drop-in replacment for Cython.Build.cythonize
    for extension in extensions:
        sources = []
        for sfile in extension.sources:
            path, ext = os.path.splitext(sfile)
            if ext in (".pyx", ".py"):
                ext = {"c++": ".cpp"}.get(extension.language, '.c')
                sfile = path + {"c++": ".cpp"}.get(extension.language, '.c')
            sources.append(sfile)
        extension.sources[:] = sources
    return extensions
~~~

See https://github.com/FedericoStra/cython-package-example/blob/master/setup.py for a complete example.

If there are other packages that `setup.py` depends on e.g. numpy for `include_dirs=[numpy.get_include()]`, there techniques for delaying their import until after `install_requires` has been processed, e.g. by using `create_extension`, [as explained in the Cython documentation](https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#configuring-the-c-build)


## Cython packages using pyproject.toml

Recently, with the adoption of [PEP 517][]/[518][PEP 518], the "build dependencies" may be specified in a file `pyproject.toml`. Build dependencies are the requirements for running `setup.py` itself, which we can use that to enforce that Cython is installed (in a particular version, if that matters), as well as any other dependencies like numpy. See [What the Heck is pyproject.toml]( https://snarky.ca/what-the-heck-is-pyproject-toml/).

Ultimately, `pyproject.toml` may replace `setup.py` and `setup.cfg` entirely, but as of Nov 2020, adaption of the new system is still lagging. Most importantly, not having a `setup.py` currently does not allow for editable installs, which are a cornerstone of the testing approach we use here.  Thus, for the time being, we only use `pyproject.toml` to specify the build dependencies.It is worth noting that [PEP 517][] uses *build isolation*: The build requirements are installed in a temporary virtual environment, not the environment running `pip` (our tox testing environment). Thus, dependencies listed in `pyproject.toml` may have to be specified separately as dev-requirements (`extras_require['dev']` in `setup.py`) such that they are installed into tox environments.

Since the ability to specify build requirements removes any need for packaging the source distribution in such a way that it can be installed without Cython, we no longer need workarounds like the `no_cythonize` function discussed above. That means that the cythonized `c` files do not have to be included in the source distribution, although doing so does not cause harm, and may be useful for the system administrator in an unusual environment when installing the package "manually".


An example of a full `pyproject.toml` file augmenting a `setup.py` file is the following:

~~~
[build-system]
requires = ["setuptools", "wheel", "cython", "numpy"]
build-backend = "setuptools.build_meta"
~~~

The `build-backend` is optional. Quoting from [PEP 517][]:

> If the `pyproject.toml` file is absent, or the build-backend key is missing, the source tree is not using this specification, and tools should revert to the legacy behaviour of running `setup.py` (either directly, or by implicitly invoking the `setuptools.build_meta:__legacy__` backend).


Generally:

* If there is no `pyproject.toml` file or Cython is not listed as a build dependency, package the cythonized c code in the source distribution and write `setup.py` such that Cython is not used by default

* If there is a `pyproject.toml` file that includes Cython in its `requires` list, the `setup.py` should be written such that Cython is used by default to cythonize the `.pyx` files in the source distribution.


[PEP 517]: https://www.python.org/dev/peps/pep-0517/
[PEP 518]: https://www.python.org/dev/peps/pep-0518/


## Building platform wheels

See https://github.com/joerick/cibuildwheel

If building via `tox`, make sure to pass the appropriate environment variables to tox.
