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


def _get_version() -> str:
    current_file = Path(__file__).resolve()

    possible_locations = [
        current_file.parent.parent.parent / "pyproject.toml",
        current_file.parent.parent.parent.parent / "pyproject.toml",
    ]

    for pyproject_path in possible_locations:
        if pyproject_path.exists():
            try:
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)

                version = data["project"]["version"]

                if not isinstance(version, str) or not version.strip():
                    raise RuntimeError(
                        f"Invalid version in {pyproject_path}: {version!r}. "
                        "Version must be a non-empty string."
                    )

                return version.strip()

            except KeyError as exc:
                available_keys = list(data.get("project", {}).keys())
                raise KeyError(
                    f"Version key not found in {pyproject_path}. "
                    f"Expected [project.version], but found: {available_keys}. "
                    f"Ensure pyproject.toml has [project] section with 'version' key."
                ) from exc

            except tomllib.TOMLDecodeError as exc:
                raise RuntimeError(
                    f"Invalid TOML syntax in {pyproject_path}: {exc}"
                ) from exc

            except Exception as exc:
                raise RuntimeError(f"Failed to parse {pyproject_path}: {exc}") from exc

    searched_paths = "\n  - ".join(str(p) for p in possible_locations)
    raise FileNotFoundError(
        f"pyproject.toml not found. Searched:\n  - {searched_paths}\n\n"
        f"If running from source, ensure you're in the project root.\n"
        f"If installed, try reinstalling: pip install --force-reinstall argparsecfg"
    )


try:
    __version__ = _get_version()
except Exception as exc:
    warnings.warn(
        f"Failed to load version from pyproject.toml: {exc}\n"
        f"Using fallback version '0.0.0.unknown'\n"
        f"This usually means pyproject.toml is missing or corrupted.",
        RuntimeWarning,
        stacklevel=2,
    )
    __version__ = "0.0.0.unknown"


__all__ = ["__version__"]
