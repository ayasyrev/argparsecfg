from __future__ import annotations

import sys
import warnings
from pathlib import Path

if sys.version_info < (3, 11):
    raise RuntimeError(
        f"Python {sys.version_info.major}.{sys.version_info.minor} is not supported. "
        "Python 3.11 or higher is required."
    )

import tomllib
from importlib.metadata import PackageNotFoundError, version


def _get_version_from_metadata() -> str | None:
    """Try to get version from importlib.metadata."""
    try:
        return version("argparsecfg")
    except PackageNotFoundError:
        return None


def _get_version_from_pyproject() -> str:
    """Fallback: Read version from pyproject.toml by traversing parent directories."""
    current_file = Path(__file__).resolve()
    current_dir = current_file.parent

    for _ in range(6):
        pyproject_path = current_dir / "pyproject.toml"
        if pyproject_path.exists():
            try:
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)
                version_str = data["project"]["version"]

                if not isinstance(version_str, str) or not version_str.strip():
                    raise RuntimeError(
                        f"Invalid version in {pyproject_path}: {version_str!r}"
                    )
                return version_str.strip()
            except KeyError as exc:
                available_keys = list(data.get("project", {}).keys())
                raise KeyError(
                    f"Version key not found in {pyproject_path}. "
                    f"Expected [project.version], found: {available_keys}"
                ) from exc
            except tomllib.TOMLDecodeError as exc:
                raise RuntimeError(
                    f"Invalid TOML syntax in {pyproject_path}: {exc}"
                ) from exc
            except Exception as exc:
                raise RuntimeError(f"Failed to parse {pyproject_path}: {exc}") from exc
        current_dir = current_dir.parent

    raise FileNotFoundError("pyproject.toml not found in parent directories")


def _get_version() -> str:
    """Get version: try metadata first, fallback to pyproject.toml."""
    metadata_version = _get_version_from_metadata()
    if metadata_version is not None:
        return metadata_version
    return _get_version_from_pyproject()


try:
    __version__ = _get_version()
except Exception as exc:
    warnings.warn(
        f"Failed to load version: {exc}. Using fallback '0.0.0.unknown'",
        RuntimeWarning,
        stacklevel=2,
    )
    __version__ = "0.0.0.unknown"


__all__ = ["__version__"]
