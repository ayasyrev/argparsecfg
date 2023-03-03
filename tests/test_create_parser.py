import argparse

from argparsecfg.core import ParserCfg, create_parser

from .test_core import compare_parsers, compare_parsers_actions


def test_create_parser_default():
    """test creation basic parser w/ default args"""
    parser_base = argparse.ArgumentParser()
    parser_cfg = ParserCfg()
    parser = create_parser(parser_cfg=parser_cfg)
    assert compare_parsers(parser_base, parser)
    assert compare_parsers_actions(parser_base, parser)
    # create parser w/o args
    parser = create_parser()
    assert compare_parsers(parser_base, parser)
    assert compare_parsers_actions(parser_base, parser)


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
    assert compare_parsers_actions(parser_base, parser)
