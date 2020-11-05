#!/usr/bin/env python3

import os
from setuptools import find_packages, setup, Extension

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

with open('README.md', encoding='utf8') as readme_file:
    README = readme_file.read()


def get_version(filename):
    """Extract the package version."""
    with open(filename, encoding='utf8') as in_fh:
        for line in in_fh:
            if line.startswith('__version__'):
                return line.split('=')[1].strip()[1:-1]
    raise ValueError("Cannot extract version from %s" % filename)


setup(
    ext_modules=EXTENSIONS,
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "dev": DEV_REQUIRES,
        "docs": ["sphinx", "sphinx-rtd-theme"],
    },
    author="Michael Goerz",
    author_email='mail@michaelgoerz.net',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
    ],
    description="Example of a package with Cython extensions",
    python_requires='>=3.7',
    long_description=README,
    long_description_content_type='text/markdown',
    name='mg-cython-package-example',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={'*': ['*.pxd', '*.h'], 'cypack': ['data/*']},
    url='https://github.com/goerz-testing/cython-package-example',
    version=get_version('./src/cypack/__init__.py'),
    zip_safe=False,
)
