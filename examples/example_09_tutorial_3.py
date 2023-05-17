# Example 9 - repeat examples from python tutorial for argparse.
# https://docs.python.org/3/howto/argparse.html#introducing-optional-arguments
# Introducing Optional arguments
import argparse
from dataclasses import dataclass

from argparsecfg import add_args_from_dc, field_argument as add_argument
from argparsecfg.core import create_dc_obj
from argparsecfg.test_tools import parsers_equal, parsers_equal_typed


# create parser
parser = argparse.ArgumentParser()
parser.add_argument("--verbosity", help="increase output verbosity")


# create config for App as dataclass
@dataclass
class AppCfg:  # type: ignore
    # as by default argparse parsed arguments from command line as str
    verbosity: str = add_argument("--verbosity", help="increase output verbosity")


# create parser and add arguments from dataclass
parser_2 = argparse.ArgumentParser()
add_args_from_dc(parser_2, AppCfg)

# parsers are equal
assert parsers_equal_typed(parser, parser_2)

# lets parse arguments
cl_arg = ["--verbosity", "1"]
# we got Namespace object from parser
args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)
assert args.verbosity == args_2.verbosity == "1"
# # but we can convert Namespace to dataclass object with types and autocomplete at ide
cfg: AppCfg = create_dc_obj(AppCfg, args)
assert cfg.verbosity == args.verbosity == "1"


# as at tutorial lets modify parser
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="increase output verbosity", action="store_true")


@dataclass
class AppCfg:  # pylint: disable=function-redefined
    verbose: bool = add_argument(
        "--verbose", help="increase output verbosity", action="store_true"
    )


parser_2 = argparse.ArgumentParser()
add_args_from_dc(parser_2, AppCfg)

assert parsers_equal(parser, parser_2)

cl_arg = ["--verbose"]

args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)
assert args.verbose == args_2.verbose
assert args.verbose is True
# # but we can convert Namespace to dataclass object with types and autocomplete at ide
cfg: AppCfg = create_dc_obj(AppCfg, args)
assert cfg.verbose == args.verbose
assert cfg.verbose is True
