from __future__ import annotations

import dataclasses
from typing import BinaryIO

import tomli_w

from tosholi.protocols import DataClassProtocol


def dump(data: DataClassProtocol, fp: BinaryIO) -> None:
    """Serialize data class as a TOML formatted stream to file-like object.

    Args:
        data: Data class instance to serialize.
        fp: File-like bytes stream to write serialized data class to.
    """
    data_dict = dataclasses.asdict(data)
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
