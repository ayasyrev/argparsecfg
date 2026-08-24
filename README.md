# ArgparseCfg

Config for argparse.

WIP

Simple wrapper for python argparse.
Use dataclass for you app config.
It gives you typed config instead of default Namespace from argparse.

You can see examples at `examples` folder - Same examples as ad python docs and tutorial for argparse.

## Version

The package version is dynamically loaded from `pyproject.toml`:

```python
from argparsecfg import __version__
print(__version__)  # "0.2.5b2"
```

**Note**: This package requires Python 3.11 or higher.
