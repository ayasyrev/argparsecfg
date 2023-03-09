import argparse
from dataclasses import dataclass

from argparsecfg.core import ParserCfg, add_args_from_dc, create_dc_obj, create_parser

from .test_tools import parsers_args_equal, parsers_actions_equal


@dataclass
class SimpleArg:
    arg_int: int
    arg_float: float = 0.0
    arg_str: str = ""


def test_add_args_simple(capsys):
    """test basic args"""
    # base parser
    parser_base = argparse.ArgumentParser()
    parser_base.add_argument("--arg_int", type=int, required=True)
    parser_base.add_argument("--arg_float", type=float, default=0.0)
    parser_base.add_argument("--arg_str", type=str, default="")

    # parser from cfg
    parser_cfg = ParserCfg()
    parser = create_parser(parser_cfg=parser_cfg)

    # add arguments - SimpleArg
    add_args_from_dc(parser, SimpleArg)
    assert parsers_args_equal(parser_base, parser)
    assert parsers_actions_equal(parser_base, parser)

    # wrong arg
    add_args_from_dc(parser, 10)
    captured = capsys.readouterr()
    assert captured.out == "Warning: <class 'int'> not dataclass type\n"


def test_parser(capsys):
    """basic parser test create dataclass instance."""
    # create parser, add args
    parser = create_parser()
    add_args_from_dc(parser, SimpleArg)
    # parse
    args = parser.parse_args(["--arg_int", "10"])
    # create obj from parsed args
    dc_obj_parsed = create_dc_obj(SimpleArg, args)
    # obj same data from dataclass
    dc_obj_default = SimpleArg(arg_int=10)
    assert dc_obj_parsed == dc_obj_default

    # wrong arg
    dc_obj_parsed = create_dc_obj(10, args)
    captured = capsys.readouterr()
    assert captured.out == "Error: <class 'int'> not dataclass type\n"
