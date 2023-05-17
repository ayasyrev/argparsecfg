# Example 11 - repeat examples from python tutorial for argparse.
# https://docs.python.org/3/howto/argparse.html#combining-positional-and-optional-arguments
# Combining Positional and Optional arguments
import argparse
from dataclasses import dataclass

from argparsecfg import add_args_from_dc, field_argument as add_argument
from argparsecfg.core import create_dc_obj, field_argument
from argparsecfg.test_tools import parsers_equal


# create parser
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int, help="display a square of a given number")
parser.add_argument(
    "-v", "--verbose", action="store_true", help="increase output verbosity"
)


# create config for App as dataclass
@dataclass
class AppCfg:  # type: ignore
    square: int = add_argument(
        "square", type=int, help="display a square of a given number"
    )
    verbose: bool = add_argument(
        "-v", "--verbose", action="store_true", help="increase output verbosity"
    )


# create parser and add arguments from dataclass
parser_2 = argparse.ArgumentParser()
add_args_from_dc(parser_2, AppCfg)

# parsers are equal
assert parsers_equal(parser, parser_2)

# parse arguments
cl_arg = ["4", "--verbose"]

args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)

assert args.verbose == args_2.verbose
assert args.verbose is True
assert args.square == args_2.square == 4
# # but we can convert Namespace to dataclass object with types and autocomplete at ide
cfg: AppCfg = create_dc_obj(AppCfg, args)
assert cfg.verbose == args.verbose
assert cfg.verbose is True
assert args.square == cfg.square == 4


# Next variant
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int, help="display a square of a given number")
parser.add_argument("-v", "--verbosity", type=int, help="increase output verbosity")


# this time we use field_argument instead of add_argument
@dataclass
class AppCfg:  # type: ignore  pylint: disable=function-redefined
    square: int = field_argument(
        "square", type=int, help="display a square of a given number"
    )
    verbosity: int = field_argument(
        "-v", "--verbosity", type=int, help="increase output verbosity"
    )


parser_2 = argparse.ArgumentParser()
add_args_from_dc(parser_2, AppCfg)

assert parsers_equal(parser, parser_2)

# parse arguments
cl_arg = ["4", "-v", "1"]

args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)

assert args.verbosity == args_2.verbosity == 1
assert args.square == args_2.square == 4

cfg: AppCfg = create_dc_obj(AppCfg, args)
assert cfg.verbosity == args.verbosity == 1
assert cfg.square == args.square == 4


# Next variant, choices
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int, help="display a square of a given number")
parser.add_argument(
    "-v", "--verbosity", type=int, choices=[0, 1, 2], help="increase output verbosity"
)


@dataclass
class AppCfg:  # type: ignore  pylint: disable=function-redefined
    square: int = field_argument(
        "square", type=int, help="display a square of a given number"
    )
    verbosity: int = field_argument(
        "-v",
        "--verbosity",
        type=int,
        choices=[0, 1, 2],
        help="increase output verbosity",
    )


parser_2 = argparse.ArgumentParser()
add_args_from_dc(parser_2, AppCfg)

assert parsers_equal(parser, parser_2)
assert parser.format_help() == parser_2.format_help()


# Next variant, count
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int, help="display the square of a given number")
parser.add_argument(
    "-v", "--verbosity", action="count", help="increase output verbosity"
)


@dataclass
class AppCfg:  # type: ignore  pylint: disable=function-redefined
    square: int = field_argument(
        "square", type=int, help="display the square of a given number"
    )
    verbosity: int = field_argument(
        "-v", "--verbosity", action="count", help="increase output verbosity"
    )


parser_2 = argparse.ArgumentParser()
add_args_from_dc(parser_2, AppCfg)

assert parsers_equal(parser, parser_2)
assert parser.format_help() == parser_2.format_help()


# parse arguments
cl_arg = ["4", "--verbosity", "--verbosity"]

args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)

assert args.verbosity == args_2.verbosity == 2

cfg: AppCfg = create_dc_obj(AppCfg, args)
assert cfg.verbosity == args.verbosity == 2

# parse arguments with short option
cl_arg = ["4", "-vvv"]

args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)

assert args.verbosity == args_2.verbosity == 3

cfg: AppCfg = create_dc_obj(AppCfg, args)
assert cfg.verbosity == args.verbosity == 3


# Next variant, count with default
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int, help="display a square of a given number")
parser.add_argument(
    "-v", "--verbosity", action="count", default=0, help="increase output verbosity"
)


@dataclass
class AppCfg:  # pylint: disable=function-redefined
    square: int = field_argument(
        "square", type=int, help="display a square of a given number"
    )
    verbosity: int = field_argument(
        "-v", "--verbosity", action="count", default=0, help="increase output verbosity"
    )


parser_2 = argparse.ArgumentParser()
add_args_from_dc(parser_2, AppCfg)

assert parsers_equal(parser, parser_2)


# parse arguments
cl_arg = ["4", "-vv"]

args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)

assert args.verbosity == args_2.verbosity == 2

cfg: AppCfg = create_dc_obj(AppCfg, args)
assert cfg.verbosity == args.verbosity == 2

# # parse arguments with default
cl_arg = ["4"]

args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)

assert args.verbosity == args_2.verbosity == 0

cfg: AppCfg = create_dc_obj(AppCfg, args)
assert cfg.verbosity == args.verbosity == 0
