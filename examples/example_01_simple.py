# Basic example - create base config for you app with dataclass.
import argparse
from dataclasses import dataclass
from argparsecfg.core import add_args_from_dc, create_dc_obj


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


if __name__ == "__main__":
    # parse arguments as usual. We got Namespace without typing
    args = parser.parse_args()
    # create dataclass object from arguments.
    cfg: AppCfg = create_dc_obj(AppCfg, args)
    # now we got object with autocompletion at ide.
    # if you want to play with config at jupyter notebook: import AppCfg.
    print(cfg)
