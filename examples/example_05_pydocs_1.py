# Example 5 - repeat python docs for argparse example.

import argparse

from dataclasses import dataclass

from argparsecfg import field_argument as add_argument

from argparsecfg import ArgumentParserCfg, add_args_from_dc, create_parser
from argparsecfg.test_tools import parsers_actions_diff, parsers_equal_typed


# create parser
parser = argparse.ArgumentParser(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)

# We can use same parser, but we can create in from config.
parser_cfg = ArgumentParserCfg(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)
parser_2 = create_parser(parser_cfg)


# basic example from docs.
parser.add_argument("filename")  # positional argument
parser.add_argument("-c", "--count")  # option that takes a value
parser.add_argument("-v", "--verbose", action="store_true")  # on/off flag


# We create config for App as dataclass
@dataclass
class AppCfg:
    filename: str = add_argument("filename")  # positional argument
    count: str = add_argument(
        "-c",
        "--count",
    )  # option that takes a value
    verbose: bool = add_argument("-v", "--verbose", action="store_true")  # on/off flag


# now we add arguments from dataclass
add_args_from_dc(parser_2, AppCfg)

# compare
assert parsers_equal_typed(parser, parser_2)

# parsers equal
# difference is [{'type': (None, <class 'str'>)}, {'type': (None, <class 'str'>)}]
# if we didn't set type at argparse it will be None at parser, after parse it will be str.
# we set type for this argument as str.
diff = parsers_actions_diff(parser, parser_2)
print(diff)
