Cython package example
======================

.. image:: https://img.shields.io/badge/goerz--testing-cython--package--example-blue?logo=github
   :alt: Source code on Github
   :target: https://github.com/goerz-testing/cython-package-example 
.. image:: https://github.com/goerz-testing/cython-package-example/workflows/Tests/badge.svg?branch=master
   :alt: Tests
   :target: https://github.com/goerz-testing/cython-package-example/actions?query=workflow%3ATests
.. image:: https://github.com/goerz-testing/cython-package-example/workflows/Docs/badge.svg?branch=master 
   :alt: Docs
   :target: https://github.com/goerz-testing/cython-package-example/actions?query=workflow%3ADocs

The purpose of this package is to demonstrate the organization of a project
developed using Cython. See the `Github project`_ for example source code and
configuration files, showing the best practices for a project that makes use of
``pyproject.toml``, how to create extension modules with Cython, how to
implement functions in C and make them available to Cython, how to include
package data, how to write a ``setup.py`` script that allows users without
Cython to install the package nonetheless.

The ideas and concepts implemented here are discussed in the Guidelines below.

.. toctree::
   :maxdepth: 3
   :caption: Guidelines

   guidelines


.. toctree::
   :maxdepth: 1
   :caption: Example API

   API/cypack

The above example API exists merely to illustrate how Sphinx will render the
API for a Cython project.

.. _Github project: https://github.com/goerz-testing/cython-package-example
