# Example 7 - repeat examples from python tutorial for argparse.
# https://docs.python.org/3/howto/argparse.html#introducing-positional-arguments
# Introducing Positional arguments
import argparse
from dataclasses import dataclass

from argparsecfg import add_args_from_dc, field_argument as add_argument
from argparsecfg.core import create_dc_obj
from argparsecfg.test_tools import parsers_equal_typed


# create parser
parser = argparse.ArgumentParser()
parser.add_argument("echo")


# create config for App as dataclass
@dataclass
class AppCfg:
    echo: str = add_argument("echo")


# create parser and add arguments from dataclass
parser_2 = argparse.ArgumentParser()
add_args_from_dc(parser_2, AppCfg)

# parsers are equal
assert parsers_equal_typed(parser, parser_2)


# lets parse arguments
cl_arg = ["argument from command line"]
# we got Namespace object from parser
args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)
assert args.echo == args_2.echo

# but we can convert Namespace to dataclass object with types and autocomplete at ide
cfg: AppCfg = create_dc_obj(AppCfg, args)
assert cfg.echo == args.echo
