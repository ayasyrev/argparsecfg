from __future__ import annotations

import argparse
from argparse import HelpFormatter, ArgumentParser
from dataclasses import is_dataclass
from functools import wraps
from inspect import signature
from typing import Any, Callable, Optional, Sequence, Type

from argparsecfg.core import (ArgumentParserCfg, add_args_from_dc,
                              create_dc_obj, create_parser)


def app(
        parser_cfg: ArgumentParserCfg | None = None,
        prog: str | None = None,
        usage: str | None = None,
        description: str | None = None,
        epilog: str | None = None,
        parents: Sequence[ArgumentParser] = [], # type: ignore  - as at argparse
        formatter_class: Type[HelpFormatter] = HelpFormatter,
        prefix_chars: str = "-",
        fromfile_prefix_chars: str | None = None,
        argument_default: str | None = None,
        conflict_handler: str = 'error',
        add_help: bool = True,
        allow_abbrev: bool = True,
        exit_on_error: bool = True,
):
    if parser_cfg is None:
        parser_cfg = ArgumentParserCfg(
            prog=prog,
            usage=usage,
            description=description,
            epilog=epilog,
            parents=parents,
            formatter_class=formatter_class,
            prefix_chars=prefix_chars,
            fromfile_prefix_chars=fromfile_prefix_chars,
            argument_default=argument_default,
            conflict_handler=conflict_handler,
            add_help=add_help,
            allow_abbrev=allow_abbrev,
            exit_on_error=exit_on_error,
        )
    # """Create app.
    # Simple variant - expecting function with one argument"""
    # to add - ags for argparse parser, ...

    def create_app(func: Callable[[Type[Any]], None]):
        sig = signature(func)
        params = [param.annotation for param in sig.parameters.values() if is_dataclass(param.annotation)]
        app_cfg = params[0]

        @wraps(func)
        def parse_and_run(args: Optional[Sequence[str]] = None) -> None:
            parser = create_parser(parser_cfg)
            add_args_from_dc(parser, app_cfg)
            parsed_args = parser.parse_args(args)
            cfg = create_dc_obj(app_cfg, parsed_args)
            func(cfg)
        return parse_and_run

    return create_app


class App:
    def __init__(
        self,
        parser_cfg: ArgumentParserCfg | None = None,
        prog: str | None = None,
        usage: str | None = None,
        description: str | None = None,
        epilog: str | None = None,
        parents: Sequence[ArgumentParser] = [], # type: ignore  - as at argparse
        formatter_class: Type[HelpFormatter] = HelpFormatter,
        prefix_chars: str = "-",
        fromfile_prefix_chars: str | None = None,
        argument_default: str | None = None,
        conflict_handler: str = 'error',
        add_help: bool = True,
        allow_abbrev: bool = True,
        exit_on_error: bool = True,
    ):
        if parser_cfg is None:
            self.parser = argparse.ArgumentParser(
                prog=prog,
                usage=usage,
                description=description,
                epilog=epilog,
                parents=parents,
                formatter_class=formatter_class,
                prefix_chars=prefix_chars,
                fromfile_prefix_chars=fromfile_prefix_chars,
                argument_default=argument_default,
                conflict_handler=conflict_handler,
                add_help=add_help,
                allow_abbrev=allow_abbrev,
                exit_on_error=exit_on_error,
            )
        else:
            self.parser = create_parser(parser_cfg)

    def main(self, func: Callable[[Type[Any]], None]):
        sig = signature(func)
        params = [param.annotation for param in sig.parameters.values() if is_dataclass(param.annotation)]
        app_cfg = params[0]
        add_args_from_dc(self.parser, app_cfg)
        self.main_func = func

        @wraps(func)
        def parse_and_run(args: Optional[Sequence[str]] = None) -> None:
            parsed_args = self.parser.parse_args(args)
            cfg = create_dc_obj(app_cfg, parsed_args)
            func(cfg)
        self.parse_and_run = parse_and_run
        return parse_and_run

    def __call__(self, args: Optional[Sequence[str]] = None) -> None:
        # self.main_func(args)
        self.parse_and_run(args)
