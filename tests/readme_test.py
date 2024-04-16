from __future__ import annotations

import dataclasses
import pathlib
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Dict
from typing import List

import tosholi


@dataclasses.dataclass
class Owner:
    name: str
    dob: datetime


@dataclasses.dataclass
class Database:
    enabled: bool
    ports: List[int]  # noqa: UP006
    temp_targets: Dict[str, float]  # noqa: UP006


@dataclasses.dataclass
class Server:
    ip: str
    role: str


@dataclasses.dataclass
class Config:
    title: str
    owner: Owner
    database: Database
    servers: Dict[str, Server]  # noqa: UP006


EXAMPLE_CONFIG = Config(
    title='TOML Example',
    owner=Owner(
        name='Tom Preston-Werner',
        dob=datetime(
            1979,
            5,
            27,
            7,
            32,
            0,
            tzinfo=timezone(-timedelta(hours=8)),
        ),
    ),
    database=Database(
        enabled=True,
        ports=[8000, 8001, 8002],
        temp_targets={'cpu': 79.5, 'case': 72.0},
    ),
    servers={
        'alpha': Server(ip='10.0.0.1', role='frontend'),
        'beta': Server(ip='10.0.0.2', role='backend'),
    },
)

EXAMPLE_CONFIG_TOML = """\
title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27 07:32:00-08:00

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
"""


def test_load(tmp_path: pathlib.Path) -> None:
    filepath = tmp_path / 'config.toml'

    with open(filepath, 'w') as f:
        f.write(EXAMPLE_CONFIG_TOML)

    with open(filepath, 'rb') as f:
        config = tosholi.load(Config, f)

    assert config == EXAMPLE_CONFIG


def test_dump_and_load(tmp_path: pathlib.Path) -> None:
    filepath = tmp_path / 'config.toml'

    with open(filepath, 'wb') as f:
        tosholi.dump(EXAMPLE_CONFIG, f)

    with open(filepath, 'rb') as f:
        config = tosholi.load(Config, f)

    assert config == EXAMPLE_CONFIG
