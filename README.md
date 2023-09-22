# Tosholi

[![tests](https://github.com/gpauloski/tosholi/actions/workflows/tests.yml/badge.svg)](https://github.com/gpauloski/tosholi/actions)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/gpauloski/tosholi/main.svg)](https://results.pre-commit.ci/latest/github/gpauloski/tosholi/main)

Tosholi is a simple library for parsing TOML files into Python dataclasses.
*Tosholi* means to interpret or translate and comes from the Chickasaw and
Choctaw languages.

## Installation

```bash
$ pip install tosholi
```

## Get Started

Coming soon.

## Developing

We use [tox](https://tox.wiki/) for testing and
[pre-commit](https://pre-commit.com/) for linting. Get started for local
development with:
```bash
$ tox --devenv venv -e py311
$ . venv/bin/activate
$ pre-commit install
```
or
```bash
$ python -m venv venv
$ . venv/bin/activate
$ pip install -e .[dev]
$ pre-commit install
```
