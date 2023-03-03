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


def compare_parsers_actions(
    parser_1: argparse.ArgumentParser,
    parser_2: argparse.ArgumentParser,
) -> bool:
    """Compare actions at two parsers"""
    actions_1 = parser_1._actions  # pylint: disable=protected-access
    actions_2 = parser_2._actions  # pylint: disable=protected-access
    if len(actions_1) != len(actions_2):
        return False
    # check order of elements
    for act_1, act_2 in zip(actions_1, actions_2):
        # pass
        if act_1.__dict__.keys() != act_2.__dict__.keys():  # is it possible?
            return False
        if not all(
            val == act_2.__dict__.get(key)
            for key, val in act_1.__dict__.items() if key != "container"
        ):
            return False
    return True


def test_create_parser_default():
    """test creation basic parser w/ default args"""
    parser_base = argparse.ArgumentParser()
    parser_cfg = ParserCfg()
    parser = create_parser(parser_cfg=parser_cfg)
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
