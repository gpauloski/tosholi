from __future__ import annotations

import dataclasses
import sys
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

import pytest

from tosholi.protocols import DataClassProtocol
from tosholi.validate import get_dataclass_fields
from tosholi.validate import get_types
from tosholi.validate import is_dict
from tosholi.validate import is_list
from tosholi.validate import is_literal
from tosholi.validate import is_optional
from tosholi.validate import is_set
from tosholi.validate import is_tuple
from tosholi.validate import is_union
from tosholi.validate import validate


def test_get_dataclass_fields() -> None:
    @dataclasses.dataclass
    class _ClassA:
        field1: int
        field2: Union[str, int]
        field3 = None

    assert get_dataclass_fields(_ClassA) == {int, Union[str, int]}


@pytest.mark.parametrize(
    ('t', 'expected'),
    (
        (Optional[str], {Optional, str}),
        (Union[str, int], {Union, str, int}),
        (Literal['abc', True], {Literal, str, bool}),
        (List[str], {List, str}),
        (Set[str], {Set, str}),
        (Tuple[str, int], {Tuple, str, int}),
        (Dict[str, int], {Dict, str, int}),
        (bool, {bool}),
    ),
)
def test_get_types_basic(t: Any, expected: set[Any]) -> None:
    assert get_types(t) == expected


@dataclasses.dataclass
class _ClassA:
    field1: int
    field2: str
    field3: List[Optional[str]]
    field4: Dict[str, int]
    field5: Tuple[Union[bytes, str], ...]
    field6: Set[float]


@dataclasses.dataclass
class _ClassB:
    field: _ClassA


@dataclasses.dataclass
class _ClassC:
    field: _ClassB


def test_get_types_nested_dataclass() -> None:
    types = {
        DataClassProtocol,
        Dict,
        Ellipsis,
        List,
        Optional,
        Set,
        Tuple,
        Union,
        bytes,
        float,
        int,
        str,
    }
    assert get_types(_ClassA) == types
    assert get_types(_ClassB) == types
    assert get_types(_ClassC) == types


def test_is_dict() -> None:
    assert is_dict(Dict[str, str])
    assert is_dict(Dict)
    assert not is_dict(str)
    assert is_dict(dict[str, str])
    assert is_dict(dict)


def test_is_literal() -> None:
    assert is_literal(Literal)
    assert is_literal(Literal['abc'])
    assert not is_literal(str)


def test_is_list() -> None:
    assert is_list(List[str])
    assert is_list(List)
    assert not is_list(str)
    assert is_list(list[str])
    assert is_list(list)


def test_is_optional() -> None:
    assert is_optional(Union[str, None])
    assert is_optional(Optional[str])
    assert not is_optional(str)
    if sys.version_info >= (3, 10):  # pragma: >=3.10 cover
        assert is_optional(str | None)


def test_is_set() -> None:
    assert is_set(Set[str])
    assert is_set(Set)
    assert not is_set(str)
    assert is_set(set[str])
    assert is_set(set)


def test_is_tuple() -> None:
    assert is_tuple(Tuple[str])
    assert is_tuple(Tuple)
    assert not is_tuple(str)
    assert is_tuple(tuple[str])
    assert is_tuple(tuple)


def test_is_union() -> None:
    assert is_union(Union[str, int])
    assert not is_union(str)
    if sys.version_info >= (3, 10):  # pragma: >=3.10 cover
        assert is_union(str | int)
        assert is_union(str | None)


def test_validate() -> None:
    @dataclasses.dataclass
    class _ClassA:
        field1: float
        field2: List[Optional[str]]
        field3: Dict[str, int]
        field4: Tuple[Union[str, int], ...]
        field5: Set[float]

    validate(_ClassA)

    @dataclasses.dataclass
    class _ClassB:
        field1: bytes

    with pytest.raises(TypeError, match='bytes'):
        validate(_ClassB)
