# Basic example - create base config for you app with dataclass.
import argparse
from dataclasses import dataclass
from argparsecfg.core import add_args_from_dc, create_dc_obj

# for tests
from argparsecfg.test_tools import parsers_equal


# Create config for App as dataclass
@dataclass
class AppCfg:
    arg_1: int = 0
    arg_2: float = 0.1
    arg_3: str = "string"


# create argparse.ArgumentParser as usual
parser = argparse.ArgumentParser()
# add arguments to parser from dataclass
add_args_from_dc(parser, AppCfg)

# Result parser will be same as below
parser_base = argparse.ArgumentParser()
parser_base.add_argument("--arg_1", type=int, default=0)
parser_base.add_argument("--arg_2", type=float, default=0.1)
parser_base.add_argument("--arg_3", type=str, default="string")


if __name__ == "__main__":
    # parse arguments as usual. We got Namespace without typing
    args_namespace = parser.parse_args()
    # create dataclass object from arguments.
    cfg: AppCfg = create_dc_obj(AppCfg, args_namespace)  # type: ignore
    # now we got object with autocompletion at ide.
    # if you want to play with config at jupyter notebook: import AppCfg.
    print(cfg)
    # lets compare parsers
    assert parsers_equal(parser_base, parser)
    # test compare results
    args_base = parser_base.parse_args()
    assert args_namespace == args_base
