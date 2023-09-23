# Tosholi

[![tests](https://github.com/gpauloski/tosholi/actions/workflows/tests.yml/badge.svg)](https://github.com/gpauloski/tosholi/actions)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/gpauloski/tosholi/main.svg)](https://results.pre-commit.ci/latest/github/gpauloski/tosholi/main)

Tosholi is a simple library for reading and writing TOML configuration
files using Python dataclasses. *Tosholi* means to interpret or translate and
comes from the Chickasaw and Choctaw languages.

## Installation

```bash
$ pip install tosholi
```

## Get Started

Create your configuration as a
[Python dataclass](https://docs.python.org/3/library/dataclasses.html).
Configuration dataclasses can be nested, but can only be made of
[TOML support types](https://docs.python.org/3/library/tomllib.html#conversion-table).


Consider the following `config.toml` that we want to read into a dataclass.
(This example is based on [toml.io](https://toml.io/en/)).

```toml
title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00

[database]
enabled = true
ports = [ 8000, 8001, 8002 ]
temp_targets = { cpu = 79.5, case = 72.0 }

[servers]

[servers.alpha]
ip = "10.0.0.1"
role = "frontend"

[servers.beta]
ip = "10.0.0.2"
role = "backend"
```

We can describe the configuration format with dataclasses.

```python
from __future__ import annotations

import dataclasses
from datetime import datetime

@dataclasses.dataclass
class Owner:
    name: str
    dob: datetime.datetime

@dataclasses.dataclass
class Database:
    enabled: bool
    ports: list[int]
    temp_targets: dict[str, float]

@dataclasses.dataclass
class Server:
    ip: str
    role: str

@dataclasses.dataclass
class Config:
    title: str
    owner: Owner
    database: Database
    servers: dict[str, Server]
```

Then the configuration file can be read using the `Config` dataclass as a
the template for parsing.

```python
with open('config.toml', 'rb') as f:
    config = tosholi.load(Config, f)
```

Similarly, we can convert in the opposite direction. A `Config` instance
can be converted to a `str` with `tosholi.dumps()` or written it to a file
with `tosholi.dump()`.

```python
import tosholi
from datetime import tzinfo

config = Config(
    title='TOML Example',
    owner=Owner(
        name='Tom Preston-Werner',
        dob=datetime(1979, 5, 27, 7, 32, 0),
    ),
    database=Database(
        enabled=True,
        ports=[8000, 8001, 8002],
        temp_targets={'cpu': 79.5, 'case': 72.0},
    ),
    servers={
        'alpha': Server(ip='10.0.0.1', role='frontend'),
        'beta': Server(ip='10.0.0.2', role='backend'),
    }
)

with open('config.toml', 'wb') as f:
    tosholi.dump(config, f)
```

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
