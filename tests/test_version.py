import re
import sys
from pathlib import Path

from argparsecfg import __version__
from argparsecfg.version import __version__ as version_direct


def test_version_exists() -> None:
    assert isinstance(__version__, str)
    assert len(__version__) > 0
    assert isinstance(version_direct, str)
    assert len(version_direct) > 0


def test_version_consistency() -> None:
    assert __version__ == version_direct


def test_version_format() -> None:
    semver_pattern = r"^\d+\.\d+\.\d+([a-zA-Z0-9_]+)?$"
    assert re.match(semver_pattern, __version__)


def test_version_matches_pyproject() -> None:
    import tomllib

    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    assert pyproject_path.exists()

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    expected_version = data["project"]["version"]
    assert __version__ == expected_version


def test_version_not_fallback() -> None:
    assert __version__ != "0.0.0.unknown"


def test_version_in_all() -> None:
    import argparsecfg

    assert "__version__" in argparsecfg.__all__


def test_python_version_requirement() -> None:
    assert sys.version_info >= (3, 11)
