#!/usr/bin/env python3

import os
from setuptools import setup, Extension

CYTHONIZE = True
# We'll cythonize by default since we can rely on Cython being installed at
# install-time: it is a build-requirement, defined in pyproject.toml. If you
# don't want to cythonize, but compile using the .c sources included in the
# package source distribution, set the CYTHONIZE environment variable, e.g.
#
#     CYTHONIZE=0 pip install ...
#
if "CYTHONIZE" in os.environ:
    print("CYTHONIZE = %s" % os.environ["CYTHONIZE"])
    if os.environ["CYTHONIZE"] == '0':
        CYTHONIZE = False

try:
    from Cython.Build import cythonize
except ImportError:
    print("WARNING: Cython not available")
    CYTHONIZE = False


def no_cythonize(extensions, **_ignore):
    """Transform extensions to use packaged pre-cythonized sources.

    This function replaces :func:`Cython.Build.cythonize` when running
    ``setup.py`` from a source distribution that packages the ``.c`` files that
    result from cythonization of ``.pyx`` files.

    Adapted from https://tinyurl.com/y4aavzq5.
    """
    # https://tinyurl.com/y4aavzq5 ->
    # https://cython.readthedocs.io/en/latest/src/userguide/
    # source_files_and_compilation.html#distributing-cython-modules
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


EXTENSIONS = [
    Extension("cypack.utils", ["src/cypack/utils.pyx"]),
    Extension("cypack.answer", ["src/cypack/answer.pyx"]),
    Extension("cypack.fibonacci", ["src/cypack/fibonacci.pyx"]),
    Extension(
        "cypack.sub.wrong",
        ["src/cypack/sub/wrong.pyx", "src/cypack/sub/helper.c"],
    ),
]


if CYTHONIZE:
    EXTENSIONS = cythonize(
        EXTENSIONS,
        compiler_directives={"language_level": 3, "embedsignature": True},
    )
else:
    print("WARNING: Not cythonizating")
    EXTENSIONS = no_cythonize(EXTENSIONS)

with open("requirements.txt") as fp:
    INSTALL_REQUIRES = fp.read().strip().split("\n")

with open("requirements-dev.txt") as fp:
    DEV_REQUIRES = fp.read().strip().split("\n")

setup(
    ext_modules=EXTENSIONS,
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "dev": DEV_REQUIRES,
        "docs": ["sphinx", "sphinx-rtd-theme"],
    },
)
