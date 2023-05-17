# Example 10 - repeat examples from python tutorial for argparse.
# https://docs.python.org/3/howto/argparse.html#short-options
# Short options
import argparse
from dataclasses import dataclass

from argparsecfg import add_args_from_dc, field_argument as add_argument
from argparsecfg.core import create_dc_obj
from argparsecfg.test_tools import parsers_equal


# create parser
parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--verbose", help="increase output verbosity", action="store_true"
)


# create config for App as dataclass
@dataclass
class AppCfg:  # type: ignore
    verbose: bool = add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )


# create parser and add arguments from dataclass
parser_2 = argparse.ArgumentParser()
add_args_from_dc(parser_2, AppCfg)

# parsers are equal
assert parsers_equal(parser, parser_2)

# parse arguments
cl_arg = ["--verbose"]

args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)
assert args.verbose == args_2.verbose
assert args.verbose is True
# # but we can convert Namespace to dataclass object with types and autocomplete at ide
cfg: AppCfg = create_dc_obj(AppCfg, args)
assert cfg.verbose == args.verbose
assert cfg.verbose is True

# with short flag
cl_arg = ["-v"]

args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)
assert args.verbose == args_2.verbose
assert args.verbose is True
# # but we can convert Namespace to dataclass object with types and autocomplete at ide
cfg: AppCfg = create_dc_obj(AppCfg, args)
assert cfg.verbose == args.verbose
assert cfg.verbose is True
