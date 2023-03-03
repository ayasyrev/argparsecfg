import argparse
from argparse import HelpFormatter
import dataclasses
from dataclasses import Field, dataclass, field, asdict
from typing import Optional


@dataclass
class ParserCfg:
    prog: Optional[str] = None
    usage: Optional[str] = None
    description: Optional[str] = None
    epilog: Optional[str] = None
    parents: list[str] = field(default_factory=list)
    formatter_class: type = HelpFormatter
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
    parser = argparse.ArgumentParser(**asdict(parser_cfg))
    return parser


def get_field_type(dc_field: Field) -> type:
    """Return field type"""
    # temp simplified
    return dc_field.type


def add_arg(parser: argparse.ArgumentParser, dc_field: Field) -> None:
    long_flag = f"{parser.prefix_chars * 2}{dc_field.name}"
    kwargs = {}
    kwargs["type"] = get_field_type(dc_field)
    if not isinstance(dc_field.default, dataclasses._MISSING_TYPE):
        kwargs["default"] = dc_field.default
    parser.add_argument(long_flag, **kwargs)


def add_args_from_dc(parser: argparse.ArgumentParser, dc: dataclass) -> None:
    for dc_field in dc.__dataclass_fields__.values():
        add_arg(parser, dc_field)
