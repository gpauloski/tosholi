from __future__ import annotations

import dataclasses
from typing import Any
from typing import ClassVar
from typing import Protocol
from typing import runtime_checkable


@runtime_checkable
class DataClassProtocol(Protocol):
    """Data Class Protocol.

    Source: https://stackoverflow.com/questions/54668000
    """

    __dataclass_fields__: ClassVar[dict[str, dataclasses.Field[Any]]]
