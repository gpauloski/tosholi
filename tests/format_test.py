from __future__ import annotations

import dataclasses
import pathlib
from typing import List

from tosholi.format import dump
from tosholi.format import dumps


@dataclasses.dataclass
class _Subsection:
    field1: float
    field2: str


@dataclasses.dataclass
class _Section:
    subsection: _Subsection
    values: List[int]  # noqa: UP006


@dataclasses.dataclass
class _Config:
    option1: bool
    option2: bool
    section: _Section


TEST_CONFIG = _Config(
    option1=True,
    option2=False,
    section=_Section(subsection=_Subsection(42.0, 'test'), values=[1, 2, 3]),
)
TEST_CONFIG_REPR = '''\
option1 = true
option2 = false

[section]
values = [
    1,
    2,
    3,
]

[section.subsection]
field1 = 42.0
field2 = "test"
'''


def test_dump(tmp_path: pathlib.Path) -> None:
    filepath = tmp_path / 'test.toml'

    with open(filepath, 'wb') as f:
        dump(TEST_CONFIG, f)

    with open(filepath) as f:
        assert f.read() == TEST_CONFIG_REPR


def test_dumps() -> None:
    assert dumps(TEST_CONFIG) == TEST_CONFIG_REPR
