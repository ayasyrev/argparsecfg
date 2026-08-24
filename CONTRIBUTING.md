# Contributing

## Version Management

The package version is stored in `pyproject.toml` under the `[project]` section:

```toml
[project]
version = "0.2.5b2"
```

**Do not modify `src/argparsecfg/version.py` directly** - it's auto-loaded from `pyproject.toml`.

### To bump the version:

1. Edit `pyproject.toml` and update the `version` field
2. Commit the change
3. The version is automatically picked up at runtime

### How it works:

- Python 3.11+ includes `tomllib` in the standard library
- At module import time, `version.py` reads `pyproject.toml`
- The version string is extracted and exposed as `__version__`
- This works in development, editable installs, and installed packages

### Python Version Support

This package requires **Python 3.11 or higher**. We use the built-in `tomllib` module, which was added in Python 3.11.
