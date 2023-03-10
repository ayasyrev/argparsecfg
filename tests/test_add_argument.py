import argparse
from dataclasses import dataclass, field

from argparsecfg.core import (ParserCfg, add_args_from_dc, create_dc_obj,
                              create_parser, ArgEnum, arg_metadata)

from .test_tools import parsers_actions_equal, parsers_args_equal


@dataclass
class ArgHelp:
    arg_int: int = field(metadata={"help": "simple help"})
    arg_float: float = field(
        default=0.0,
        metadata={ArgEnum.help: "simple help"},
    )
    arg_str: str = field(
        default="",
        metadata=arg_metadata(help="simple help"),
    )


def test_add_args_simple():
    """test basic args"""
    # base parser
    parser_base = argparse.ArgumentParser()
    parser_base.add_argument("--arg_int", type=int, required=True, help="simple help")
    parser_base.add_argument("--arg_float", type=float, default=0.0, help="simple help")
    parser_base.add_argument("--arg_str", type=str, default="", help="simple help")

    # parser from cfg
    parser_cfg = ParserCfg()
    parser = create_parser(parser_cfg=parser_cfg)

    # add arguments - ArgHelp
    add_args_from_dc(parser, ArgHelp)
    assert parsers_args_equal(parser_base, parser)
    assert parsers_actions_equal(parser_base, parser)
    assert parser_base.format_help() == parser.format_help()


def test_parser():
    """basic parser test create dataclass instance."""
    # create parser, add args
    parser = create_parser()
    add_args_from_dc(parser, ArgHelp)
    # parse
    args = parser.parse_args(["--arg_int", "10"])
    # create obj from parsed args
    dc_obj_parsed = create_dc_obj(ArgHelp, args)
    # obj same data from dataclass
    dc_obj_default = ArgHelp(arg_int=10)
    assert dc_obj_parsed == dc_obj_default
