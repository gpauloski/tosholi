from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any
from typing import BinaryIO
from typing import TypeVar

import dacite

if sys.version_info >= (3, 11):  # pragma: >=3.11 cover
    import tomllib
else:  # pragma: <3.11 cover
    import tomli as tomllib

from tosholi.protocols import DataClassProtocol
from tosholi.validate import validate

DataClassT = TypeVar('DataClassT', bound=DataClassProtocol)


def load(model: type[DataClassT], fp: BinaryIO) -> DataClassT:
    """Parse TOML from a binary file to a data class.

    Args:
        model: Data class type to parse TOML using.
        fp: File-like bytes stream to read in.

    Returns:
        Data class instance.

    Raises:
        TypeError: if `model` contains non-TOML compatible types.
    """
    return loads(model, fp.read().decode())


def loads(model: type[DataClassT], data: str) -> DataClassT:
    """Parse TOML string to data class.

    Args:
        model: Data class type to parse TOML using.
        data: TOML string to parse.

    Returns:
        Data class instance.

    Raises:
        TypeError: if `model` contains non-TOML compatible types.
    """
    validate(model)
    fields = tomllib.loads(data)
    return parse(model, fields)


def parse(model: type[DataClassT], data: Mapping[str, Any]) -> DataClassT:
    """Parse mapping into data class.

    Args:
        model: Data class type to parse mapping using.
        data: Mapping to parse.

    Returns:
        Data class instance.
    """
    return dacite.from_dict(data_class=model, data=data)
