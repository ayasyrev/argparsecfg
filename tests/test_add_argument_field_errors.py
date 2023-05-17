# pylint: disable=protected-access
import argparse
from dataclasses import dataclass

from _pytest.capture import CaptureFixture

from argparsecfg.core import (
    ArgumentParserCfg,
    add_args_from_dc,
    add_argument_metadata,
    create_dc_obj,
    create_parser,
    field_argument,
)
from argparsecfg.test_tools import (
    parsers_actions_diff,
    parsers_actions_equal,
    parsers_args_equal,
    parsers_equal,
    parsers_equal_typed,
)


def test_flag():
    """test add flag"""
    @dataclass
    class ArgFlag:
        arg_1: int = field_argument("--arg_1", flag="a")
    parser = create_parser()
    add_args_from_dc(parser, ArgFlag)
    assert "-a" in parser._option_string_actions
    assert "--arg_1" in parser._option_string_actions


def test_flag_2_useless(capsys: CaptureFixture[str]):
    """test add flag useless"""
    @dataclass
    class ArgFlag:
        arg_1: int = field_argument("-a", "--arg_1", flag="a")
    parser = create_parser()
    add_args_from_dc(parser, ArgFlag)
    assert "-a" in parser._option_string_actions
    assert "--arg_1" in parser._option_string_actions
    captured = capsys.readouterr()
    out = captured.out
    assert "got `flag` -a but args: ('-a', '--arg_1') given" in out


def test_flag_3_wrong_dc_name(capsys: CaptureFixture[str]):
    """test add flag different from dc name"""
    @dataclass
    class ArgFlag:
        arg_2: int = field_argument("-a", "--arg_1")
    parser = create_parser()
    add_args_from_dc(parser, ArgFlag)
    assert "-a" in parser._option_string_actions
    assert "--arg_1" not in parser._option_string_actions
    assert "--arg_2" in parser._option_string_actions
    captured = capsys.readouterr()
    out = captured.out
    assert "got `flag` --arg_1 but dc name is arg_2" in out
