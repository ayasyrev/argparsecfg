# Example 3 - create config with dataclass, arguments options as fields.
import argparse  # only for tests

from dataclasses import dataclass

from argparsecfg.core import (
    ArgumentParserCfg,
    add_argument_metadata,
    field_argument,
    parse_args,
)

# for tests
from argparsecfg.core import add_args_from_dc, create_parser
from argparsecfg.test_tools import parsers_equal


# Create config for parser
parser_cfg = ArgumentParserCfg(
    prog="name", description="example prog", epilog="nothing done, just example..."
)


# Create config for App as dataclass
@dataclass
class AppCfg:
    arg_1: int = field_argument(
        default=0,
        help="argument 1, int",
    )
    arg_2: float = field_argument(
        default=0.0,
        # you can use metadata.
        metadata=add_argument_metadata(help="argument 2, float"),
    )
    arg_3: str = field_argument(
        default="",
        # flag - "-s" or just "s"
        flag="s",
        help="string arg, can be used with short flag -s",
    )


# result parser will be same as below
parser_base = argparse.ArgumentParser(
    prog="name", description="example prog", epilog="nothing done, just example..."
)
parser_base.add_argument("--arg_1", type=int, default=0, help="argument 1, int")
parser_base.add_argument("--arg_2", type=float, default=0.0, help="argument 2, float")
parser_base.add_argument(
    "-s",
    "--arg_3",
    type=str,
    default="",
    help="string arg, can be used with short flag -s",
)


if __name__ == "__main__":
    # parse arguments.
    # parse_args return dataclass object from dataclass sent to it as argument.
    cfg: AppCfg = parse_args(AppCfg, parser_cfg=parser_cfg)
    # now we got object with autocompletion at ide.
    # if you want to play with config at jupyter notebook: import AppCfg.
    print(cfg)

    # Tests
    args_base = parser_base.parse_args()
    parser = create_parser(parser_cfg)
    add_args_from_dc(parser, AppCfg)
    assert parsers_equal(parser, parser_base)
    args = parser.parse_args()
    assert args == args_base
