import argparse
import dataclasses
import sys
from argparse import HelpFormatter
from dataclasses import Field, asdict, dataclass, field
from typing import Any, List, Optional, Type


@dataclass
class ParserCfg:
    """Config schema for argparse parser"""

    prog: Optional[str] = None
    usage: Optional[str] = None
    description: Optional[str] = None
    epilog: Optional[str] = None
    parents: List[str] = field(default_factory=list)
    formatter_class: Type[HelpFormatter] = HelpFormatter
    prefix_chars: str = "-"
    fromfile_prefix_chars: Optional[bool] = None
    argument_default: Optional[str] = None
    conflict_handler: str = "error"
    add_help: bool = True
    allow_abbrev: bool = True
    exit_on_error: bool = True


def create_parser(parser_cfg: Optional[ParserCfg] = None) -> argparse.ArgumentParser:
    """Create argparse parser."""
    if parser_cfg is None:
        parser_cfg = ParserCfg()
    # check if subclass -> filter args
    kwargs = asdict(parser_cfg)
    if sys.version_info.minor < 9:  # from python 3.9
        kwargs.pop("exit_on_error")  # pragma: no cover
    parser = argparse.ArgumentParser(**kwargs)
    return parser


def get_field_type(dc_field: Field) -> Type[Any]:
    """Return field type"""
    # temp simplified
    return dc_field.type


def add_arg(parser: argparse.ArgumentParser, dc_field: Field) -> None:
    """add argument to parser from dataclass field"""
    long_flag = f"{parser.prefix_chars * 2}{dc_field.name}"
    kwargs: dict[str, Any] = {}
    kwargs["type"] = get_field_type(dc_field)
    if isinstance(dc_field.default, dataclasses._MISSING_TYPE):  # pylint: disable=protected-access
        kwargs["required"] = True
    else:
        kwargs["default"] = dc_field.default
    parser.add_argument(long_flag, **kwargs)


def add_args_from_dc(parser: argparse.ArgumentParser, dc: Type[Any]) -> None:
    """add arguments tu parser from dataclass fields"""
    if dataclasses.is_dataclass(dc):
        for dc_field in dc.__dataclass_fields__.values():
            add_arg(parser, dc_field)
    else:
        print(f"Warning: {type(dc)} not dataclass type")  # ? warning ?


def create_dc_obj(dc: Type[Any], args: argparse.Namespace) -> object:
    """create dataclass instance from argparse cfg"""
    if not dataclasses.is_dataclass(dc):
        print(f"Error: {type(dc)} not dataclass type")
        return None  # ? raise error ?
    kwargs = {
        key: val for key, val in args.__dict__.items() if key in dc.__dataclass_fields__
    }
    return dc(**kwargs)
