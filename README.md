# Cython package example

![Tests](https://github.com/goerz-testing/cython-package-example/workflows/Tests/badge.svg?branch=master)
![Docs](https://github.com/goerz-testing/cython-package-example/workflows/Docs/badge.svg?branch=master)

Forked from https://github.com/FedericoStra/cython-package-example

## Purpose

The purpose of this package is to demonstrate the organization of a project developed using Cython.

It shows a suitable folder structure according to the best practices for a project that makes use of `pyproject.toml`, how to create extension modules with Cython, how to implement functions in C and make them available to Cython, how to include package data, how to write a `setup.py` script that allows users without Cython to install the package nonetheless.

The ideas and concepts implemented here are discussed in the [Documentation](https://goerz-testing.github.io/cython-package-example)

## Usage

Run `make` or `tox -av` for an overview of available development/packaging tasks.
