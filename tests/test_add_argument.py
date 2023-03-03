import argparse
from dataclasses import dataclass

from argparsecfg.core import ParserCfg, add_args_from_dc, create_parser

from .test_core import compare_parsers, compare_parsers_actions


@dataclass
class SimpleArg:
    arg_int: int
    arg_float: float = 0.
    arg_str: str = ""


def test_add_args_simple():
    """test basic args"""
    parser_base = argparse.ArgumentParser()
    parser_base.add_argument("--arg_int", type=int)
    parser_base.add_argument("--arg_float", type=float, default=0.)
    parser_base.add_argument("--arg_str", type=str, default="")

    parser_cfg = ParserCfg()
    parser = create_parser(parser_cfg=parser_cfg)
    add_args_from_dc(parser, SimpleArg)

    assert compare_parsers(parser_base, parser)
    assert compare_parsers_actions(parser_base, parser)
