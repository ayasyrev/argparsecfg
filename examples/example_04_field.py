# Example 3 - create config with dataclass, arguments options as fields.
from dataclasses import dataclass

from argparsecfg.core import (
    ArgumentParserCfg,
    add_argument_metadata,
    field_argument,
    parse_args,
)

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


if __name__ == "__main__":
    # parse arguments.
    # parse_args return dataclass object from dataclass sent to it as argument.
    cfg: AppCfg = parse_args(AppCfg, parser_cfg=parser_cfg)
    # now we got object with autocompletion at ide.
    # if you want to play with config at jupyter notebook: import AppCfg.
    print(cfg)
