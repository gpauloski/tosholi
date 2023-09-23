from __future__ import annotations

import dataclasses
import datetime
import sys
import types
import typing
from collections import defaultdict

from tosholi.protocols import DataClassProtocol

TomlTypes = {
    # Primitive types
    str,
    int,
    float,
    bool,
    datetime.datetime,
    Ellipsis,
    # Container types
    typing.List,
    typing.Tuple,
    typing.Set,
    typing.Dict,
    DataClassProtocol,
    # Other types
    typing.Optional,
    typing.Union,
}

TypeLike = typing.Union[typing.Type[typing.Any], typing.Any]


def get_dataclass_fields(cls: type[DataClassProtocol]) -> set[TypeLike]:
    """Get set of all Data Class field types.

    Source: https://github.com/yukinarit/pyserde/blob/2855b6b9041263c9d01f944216954347d00085a1/serde/compat.py#L327
    """
    types: set[TypeLike] = set()
    raw_fields = dataclasses.fields(cls)
    resolved_hints = typing.get_type_hints(cls)
    for field in raw_fields:
        real_type = resolved_hints.get(field.name)
        if real_type is not None:  # pragma: no branch
            types.add(real_type)
    return types


def get_types(cls: TypeLike) -> set[TypeLike]:
    """Get set of all types recursively.

    Source: https://github.com/yukinarit/pyserde/blob/2855b6b9041263c9d01f944216954347d00085a1/serde/compat.py#L360
    """
    types: set[TypeLike] = set()

    def _recurse(cls: TypeLike) -> None:  # noqa: PLR0912
        if cls in types:
            return

        if isinstance(cls, DataClassProtocol):
            types.add(DataClassProtocol)
            for field in get_dataclass_fields(cls):  # type: ignore[arg-type]
                _recurse(field)
        elif is_optional(cls):
            types.add(typing.Optional)
            args = typing.get_args(cls)
            if len(args) > 0:  # pragma: no branch
                _recurse(args[0])
        elif is_union(cls):
            types.add(typing.Union)
            for arg in typing.get_args(cls):
                _recurse(arg)
        elif is_list(cls):
            types.add(typing.List)
            args = typing.get_args(cls)
            if len(args) > 0:  # pragma: no branch
                _recurse(args[0])
        elif is_set(cls):
            types.add(typing.Set)
            args = typing.get_args(cls)
            if len(args) > 0:  # pragma: no branch
                _recurse(args[0])
        elif is_tuple(cls):
            types.add(typing.Tuple)
            for arg in typing.get_args(cls):
                _recurse(arg)
        elif is_dict(cls):
            types.add(typing.Dict)
            args = typing.get_args(cls)
            if len(args) == 2:  # pragma: no branch  # noqa: PLR2004
                _recurse(args[0])
                _recurse(args[1])
        else:
            types.add(cls)

    _recurse(cls)
    return types


def is_dict(t: TypeLike) -> bool:
    """Check if type is dict or defaultdict.

    Reference: https://github.com/yukinarit/pyserde/blob/2855b6b9041263c9d01f944216954347d00085a1/serde/compat.py#L685
    """
    try:
        return issubclass(
            typing.get_origin(t),  # type: ignore[arg-type]
            (dict, defaultdict),
        )
    except TypeError:
        return t in (dict, defaultdict, typing.Dict, typing.DefaultDict)


def is_list(t: TypeLike) -> bool:
    """Check if type is list.

    Reference: https://github.com/yukinarit/pyserde/blob/2855b6b9041263c9d01f944216954347d00085a1/serde/compat.py#L569
    """
    try:
        return issubclass(typing.get_origin(t), list)  # type: ignore[arg-type]
    except TypeError:
        return t in (list, typing.List)


def is_optional(t: TypeLike) -> bool:
    """Check if type is optional.

    Reference: https://stackoverflow.com/a/76397722
    """
    origin = typing.get_origin(t)
    if origin is typing.Union:
        return type(None) in typing.get_args(t)
    if (
        sys.version_info >= (3, 10) and origin is types.UnionType
    ):  # pragma: >=3.10 cover
        return type(None) in typing.get_args(t)
    return False


def is_set(t: TypeLike) -> bool:
    """Check if type is set or frozenset.

    Reference: https://github.com/yukinarit/pyserde/blob/2855b6b9041263c9d01f944216954347d00085a1/serde/compat.py#L638
    """
    try:
        return issubclass(
            typing.get_origin(t),  # type: ignore[arg-type]
            (set, frozenset),
        )
    except TypeError:
        return t in (set, frozenset, typing.Set, typing.FrozenSet)


def is_tuple(t: TypeLike) -> bool:
    """Check if type is tuple.

    Reference: https://github.com/yukinarit/pyserde/blob/2855b6b9041263c9d01f944216954347d00085a1/serde/compat.py#L598
    """
    try:
        return issubclass(typing.get_origin(t), tuple)  # type: ignore[arg-type]
    except TypeError:
        return t in (tuple, typing.Tuple)


def is_union(t: TypeLike) -> bool:
    """Check if type is union."""
    origin = typing.get_origin(t)
    if origin is typing.Union:
        return True
    if (
        sys.version_info >= (3, 10) and origin is types.UnionType
    ):  # pragma: >=3.10 cover
        return True
    return False


def validate(model: type[DataClassProtocol]) -> None:
    """Validate a Data Class type is TOML compatible.

    Python's TOML parsing supports a limited number of Python types described
    here: https://docs.python.org/3/library/tomllib.html#conversion-table.
    This function validates that a Data Class type contains only those
    supported types. This validation works recursively.

    Args:
        model: Data Class type to validate.

    Raises:
        TypeError: if `model` contains a non-TOML compatible type.
    """
    all_types = get_types(model)
    remainder = all_types - TomlTypes
    if len(remainder) > 0:
        raise TypeError(
            f'{model.__name__} contains the following non-TOML compatible '
            f'types: {", ".join(str(t) for t in remainder)}',
        )
