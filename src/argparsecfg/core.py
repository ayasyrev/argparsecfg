import argparse
from argparse import HelpFormatter
from dataclasses import dataclass, field, asdict
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
    parser = argparse.ArgumentParser(**asdict(parser_cfg))
    return parser
