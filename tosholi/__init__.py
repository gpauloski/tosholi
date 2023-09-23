from __future__ import annotations

import importlib.metadata as importlib_metadata

from tosholi.format import dump
from tosholi.format import dumps
from tosholi.parse import load
from tosholi.parse import loads
from tosholi.parse import parse

__version__ = importlib_metadata.version('tosholi')
