from __future__ import annotations

from importlib import metadata
from importlib.metadata import PackageNotFoundError


try:
    __version__ = metadata.version("argparsecfg")
except PackageNotFoundError:
    __version__ = "0.0.0"
