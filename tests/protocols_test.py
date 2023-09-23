from __future__ import annotations

import dataclasses

from tosholi.protocols import DataClassProtocol


class _TestClass:
    pass


@dataclasses.dataclass
class _TestDataClass:
    pass


def test_dataclass_protocol() -> None:
    assert not isinstance(_TestClass, DataClassProtocol)
    assert not isinstance(_TestClass(), DataClassProtocol)
    assert isinstance(_TestDataClass, DataClassProtocol)
    assert isinstance(_TestDataClass(), DataClassProtocol)
