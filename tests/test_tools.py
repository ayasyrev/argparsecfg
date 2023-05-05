import argparse

from argparsecfg.test_tools import parsers_args_equal, parsers_actions_equal, parsers_equal


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


def test_parsers_equal():
    """test parsers_equal"""
    parser_1 = argparse.ArgumentParser()
    parser_2 = argparse.ArgumentParser()
    assert parsers_equal(parser_1, parser_2)
    parser_1.add_argument("arg1")
    assert not parsers_equal(parser_1, parser_2)
    parser_2.add_argument("arg1")
    assert parsers_equal(parser_1, parser_2)
