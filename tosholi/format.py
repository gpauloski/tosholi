from __future__ import annotations

import dataclasses
from typing import Any
from typing import BinaryIO

import tomli_w

from tosholi.protocols import DataClassProtocol


def _scrub(obj: Any) -> None:
    # https://stackoverflow.com/a/20692955
    if isinstance(obj, dict):
        for key in list(obj.keys()):
            if obj[key] is None:
                del obj[key]
            else:
                _scrub(obj[key])


def dump(data: DataClassProtocol, fp: BinaryIO) -> None:
    """Serialize data class as a TOML formatted stream to file-like object.

    Args:
        data: Data class instance to serialize.
        fp: File-like bytes stream to write serialized data class to.
    """
    data_dict = dataclasses.asdict(data)
    _scrub(data_dict)
    tomli_w.dump(data_dict, fp)


def dumps(data: DataClassProtocol) -> str:
    """Serialize data class to a TOML formatted string.

    Args:
        data: Data class instance to serialize.

    Returns:
        TOML string of data class.
    """
    data_dict = dataclasses.asdict(data)
    return tomli_w.dumps(data_dict)
