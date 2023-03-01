import argparse

from argparsecfg.core import ParserCfg, create_parser


def compare_parsers(
    parser_1: argparse.ArgumentParser,
    parser_2: argparse.ArgumentParser,
) -> bool:
    """compare two parsers, return True if equal."""
    for attr in parser_1.__dict__:
        if not attr.startswith("_"):
            if getattr(parser_1, attr) != getattr(parser_2, attr):
                return False
    return True


def test_create_parser_default():
    """test creation basic parser w/ default args"""
    parser_base = argparse.ArgumentParser()
    parser_cfg = ParserCfg()
    parser = create_parser(parser_cfg=parser_cfg)
    assert compare_parsers(parser_base, parser)
    assert len(parser_base._actions) == len(parser._actions)


def test_create_parser():
    """test creation basic parser"""
    prog_name = "name"
    description = "Dummy prog."
    epilog = "nothing done..."
    parser_base = argparse.ArgumentParser(
        prog=prog_name,
        description=description,
        epilog=epilog
    )
    parser_cfg = ParserCfg(
        prog=prog_name,
        description=description,
        epilog=epilog,
    )
    parser = create_parser(parser_cfg=parser_cfg)
    assert compare_parsers(parser_base, parser)
    assert len(parser_base._actions) == len(parser._actions)
