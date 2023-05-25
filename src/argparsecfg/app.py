from __future__ import annotations

from dataclasses import is_dataclass
from inspect import signature
from typing import Any, Callable, Optional, Sequence, Type

from argparsecfg.core import ArgumentParserCfg, add_args_from_dc, create_dc_obj, create_parser


def app(parser_cfg: ArgumentParserCfg | None = None,):
    if parser_cfg is None:
        parser_cfg = ArgumentParserCfg()
    # """Create app.
    # Simple variant - expecting function with one argument"""
    # to add - args for argparse parser, ...

    def create_app(func: Callable[[Type[Any]], None]):

        sig = signature(func)
        params = [param.annotation for param in sig.parameters.values() if is_dataclass(param.annotation)]
        app_cfg = params[0]

        def parse_and_run(args: Optional[Sequence[str]] = None) -> None:
            parser = create_parser(parser_cfg)
            add_args_from_dc(parser, app_cfg)
            parsed_args = parser.parse_args(args)
            cfg = create_dc_obj(app_cfg, parsed_args)
            func(cfg)
        return parse_and_run

    return create_app
