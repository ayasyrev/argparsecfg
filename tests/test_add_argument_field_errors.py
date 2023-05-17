# pylint: disable=protected-access
from dataclasses import dataclass

from _pytest.capture import CaptureFixture

from argparsecfg.core import (
    add_args_from_dc,
    create_parser,
    field_argument,
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


def test_wrong_dest(capsys: CaptureFixture[str]):
    """test add flag different from dc name"""

    @dataclass
    class ArgFlag:
        arg_1: int = field_argument("arg_2")

    parser = create_parser()
    add_args_from_dc(parser, ArgFlag)
    assert parser._actions[1].dest == "arg_1"
    captured = capsys.readouterr()
    out = captured.out
    assert "arg `dest` arg_2 but dc name is arg_1" in out
