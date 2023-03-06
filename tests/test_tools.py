import argparse


def parsers_args_equal(
    parser_1: argparse.ArgumentParser,
    parser_2: argparse.ArgumentParser,
) -> bool:
    """compare two parsers, return True if equal."""
    for attr in parser_1.__dict__:
        if not attr.startswith("_"):
            if getattr(parser_1, attr) != getattr(parser_2, attr):
                return False
    return True


def parsers_actions_equal(
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
        if not all(
            val == act_2.__dict__.get(key)
            for key, val in act_1.__dict__.items()
            if key != "container"
        ):
            return False
    return True


def test_args_equal():
    """test parsers_args_equal"""
    parser_1 = argparse.ArgumentParser()
    parser_2 = argparse.ArgumentParser()
    assert parsers_args_equal(parser_1, parser_2)
    parser_2 = argparse.ArgumentParser(prog="test_name")
    assert not parsers_args_equal(parser_1, parser_2)


def test_parsers_actions_equal():
    """test parsers_actions_equal"""
    parser_1 = argparse.ArgumentParser()
    parser_2 = argparse.ArgumentParser()
    # initial - only help action
    assert parsers_actions_equal(parser_1, parser_2)
    # different len
    parser_1.add_argument("arg1")
    assert not parsers_actions_equal(parser_1, parser_2)
    # again the same
    parser_2.add_argument("arg1")
    assert parsers_actions_equal(parser_1, parser_2)
    # different args
    parser_1.add_argument("arg2")
    parser_2.add_argument("arg3")
    assert not parsers_actions_equal(parser_1, parser_2)
