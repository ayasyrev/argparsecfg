# Example 6 - repeat python docs for argparse example.
# https://docs.python.org/3/library/argparse.html#example
# Example
import argparse

from dataclasses import dataclass

from argparsecfg import field_argument as add_argument

from argparsecfg import ArgumentParserCfg, add_args_from_dc, create_parser
from argparsecfg.test_tools import parsers_equal


# create parser
parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument(
    "integers", metavar="N", type=int, nargs="+", help="an integer for the accumulator"
)
parser.add_argument(
    "--sum",
    dest="accumulate",
    action="store_const",
    const=sum,
    default=max,
    help="sum the integers (default: find the max)",
)


# We can use same parser, but we can create in from config.
parser_cfg = ArgumentParserCfg(
    description="Process some integers.",
)
parser_2 = create_parser(parser_cfg)


# We create config for App as dataclass
@dataclass
class AppCfg:
    integers: int = add_argument(
        "integers",
        metavar="N",
        type=int,  # type: ignore
        nargs="+",
        help="an integer for the accumulator",
    )
    sum: int = add_argument(
        "--sum",
        dest="accumulate",
        action="store_const",
        const=sum,
        default=max,
        help="sum the integers (default: find the max)",
    )


# now we add arguments from dataclass
add_args_from_dc(parser_2, AppCfg)

# compare
assert parsers_equal(parser, parser_2)
