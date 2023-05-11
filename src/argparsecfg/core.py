from __future__ import annotations

import argparse
import dataclasses
import sys
from argparse import HelpFormatter
from dataclasses import MISSING, Field, asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple, Type, Union

_MISSING_TYPE = type(MISSING)
ARG_KEYWORDS = (
    "action",
    "action",
    "nargs",
    "const",
    "default",
    "type",
    "choices",
    "required",
    "help",
    "metavar",
    "dest",
    "version",
    # not in argparse, for flags
    "flag",
    "name_or_flags",
)


@dataclass
class ArgumentParserCfg:
    """Config schema for argparse parser.
    Parameters same as at argparse.ArgumentParser.
    """

    prog: Optional[str] = None
    usage: Optional[str] = None
    description: Optional[str] = None
    epilog: Optional[str] = None
    parents: List[str] = field(default_factory=list)
    formatter_class: Type[HelpFormatter] = HelpFormatter
    prefix_chars: str = "-"
    fromfile_prefix_chars: Optional[bool] = None
    argument_default: Optional[str] = None
    conflict_handler: str = "error"
    add_help: bool = True
    allow_abbrev: bool = True
    exit_on_error: bool = True


def create_parser(
    parser_cfg: Optional[ArgumentParserCfg] = None,
) -> argparse.ArgumentParser:
    """Create argparse parser."""
    if parser_cfg is None:
        parser_cfg = ArgumentParserCfg()
    # check if subclass -> filter args
    kwargs = asdict(parser_cfg)
    if sys.version_info.minor < 9:  # from python 3.9
        kwargs.pop("exit_on_error")  # pragma: no cover
    parser = argparse.ArgumentParser(**kwargs)
    return parser


def get_field_type(dc_field: Field[Any]) -> Type[Any]:
    """Return field type"""
    # temp simplified
    return dc_field.type


def add_argument_metadata(
    *name_or_flags: Optional[str],
    flag: Optional[str] = None,
    action: Optional[str] = None,
    nargs: Optional[int] = None,
    const: Optional[str] = None,
    default: Optional[Any] = None,
    type: Union[  # pylint: disable=redefined-builtin
        str, argparse.FileType, None
    ] = None,
    choices: Optional[Iterable[Any]] = None,
    required: Optional[bool] = None,
    help: Optional[str] = None,  # pylint: disable=redefined-builtin
    metavar: Union[str, Tuple[str, ...], None] = None,
    dest: Optional[str] = None,
    # version: Optional[str] = None,  # pylint: disable=unused-argument  # not implemented
) -> Dict[str, Any]:
    """create dict with args for argparse.add_argument"""
    # if not name_or_flags:
    #     name_or_flags = None
    kwargs = {
        "name_or_flags": name_or_flags if name_or_flags else None,
        "flag": flag,
        "action": action,
        "nargs": nargs,
        "const": const,
        "default": default,
        "type": type,
        "choices": choices,
        "required": required,
        "help": help,
        "metavar": metavar,
        "dest": dest,
        # 'version': version
    }
    return {key: val for key, val in kwargs.items() if val is not None}


def filter_metadata(
    metadata: Mapping[str, Any],
) -> Dict[str, Any]:
    return {key: val for key, val in metadata.items() if key in ARG_KEYWORDS}


def process_flags(kwargs: Dict[str, Any], prefix: str = "-") -> Dict[str, Any]:
    """Process flags.
    Remove `name_or_flags`, add `flags` if need."""
    flag = kwargs.pop("flag", None)
    if flag is not None:
        if not flag.startswith(prefix):
            flag = f"{prefix}{flag}"
    name_or_flags = kwargs.pop("name_or_flags", None)

    if name_or_flags is not None:
        if len(name_or_flags) == 1:
            if name_or_flags[0][0] != prefix:  # positional. If `dest` exist we rewrite it.
                kwargs["dest"] = name_or_flags[0]
            else:
                if flag is not None:
                    kwargs["flags"] = (flag, name_or_flags[0])
                else:
                    kwargs["flags"] = name_or_flags

        else:  # if two item - flag is useless
            if flag is not None:
                print(f"Warning: got `flag` arg {flag} but args: {name_or_flags} given")
            kwargs["flags"] = name_or_flags
    else:
        if flag is not None:
            kwargs["flags"] = (flag,)
    return kwargs


def validate_kwargs(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """validate kwargs"""
    action = kwargs.get("action", None)
    if action in ("store_true", "store_false"):
        kwargs.pop("type", None)
        kwargs.pop("default", None)
    return kwargs


def kwargs_add_dc_flag(
        kwargs: Dict[str, Any],
        name: str,
        # arg_type: Type[Any],
        # default: Any,
        prefix: str = "-",
) -> Dict[str, Any]:
    """add flag from dataclass to kwargs"""
    # positional = False
    flags = kwargs.pop("flags", None)
    if flags is None:
        if kwargs.get("dest", None):  # positional
            # positional = True
            if kwargs["dest"] != name:
                print(f"Warning: {kwargs['dest']} but dc name is {name}")
        else:
            kwargs["flags"] = (f"{prefix*2}{name}",)
    elif len(flags) == 1:
        kwargs["flags"] = (*flags, f"{prefix*2}{name}")
    else:
        if flags[1] != f"{prefix*2}{name}":
            print(f"Warning: {flags[1]} but dc name is {name}")
        kwargs["flags"] = (flags[0], f"{prefix*2}{name}")
    return kwargs


def kwargs_add_dc_data(
        kwargs: Dict[str, Any],
        name: str,
        arg_type: Type[Any],
        default: Any,
) -> Dict[str, Any]:
    """add data from dataclass to kwargs"""
    dest = kwargs.get("dest", None)
    # check and set type
    metadata_type = kwargs.get("type", None)
    if metadata_type is not None:
        if metadata_type != arg_type:
            print(f"Warning: arg {name} type is {arg_type}, but at metadata {metadata_type}")
    kwargs["type"] = arg_type
    metadata_default = kwargs.get("default", None)
    if metadata_default is not None and default is None:
        print(f"Warning: arg {name} default={metadata_default} but dc default is None")
    if default is not None:
        if metadata_default is not None and metadata_default != default:
            print(f"Warning: arg {name} default={default}, but at metadata={metadata_default}")
        kwargs["default"] = default
    # else:  # required or positional
    #     if dest is None:
    #         kwargs["required"] = True
    return kwargs


def add_arg(parser: argparse.ArgumentParser, dc_field: Field[Any]) -> None:
    """add argument to parser from dataclass field"""
    if dc_field.metadata:
        kwargs = filter_metadata(dc_field.metadata)
        kwargs = process_flags(kwargs, parser.prefix_chars)
    else:
        kwargs: dict[str, Any] = {}
    # validate and set kwargs
    # data from dataclass - flag / name, type, default
    field_type = get_field_type(dc_field)
    if isinstance(dc_field.default, _MISSING_TYPE):
        default = None
    else:
        default = dc_field.default

    kwargs = kwargs_add_dc_flag(kwargs, dc_field.name, parser.prefix_chars)
    kwargs = kwargs_add_dc_data(kwargs, dc_field.name, field_type, default)
    kwargs = validate_kwargs(kwargs)

    flags = kwargs.pop("flags", [])
    parser.add_argument(*flags, **kwargs)


def add_args_from_dc(parser: argparse.ArgumentParser, dc: Type[Any]) -> None:
    """add arguments to parser from dataclass fields"""
    if dataclasses.is_dataclass(dc):
        for dc_field in dc.__dataclass_fields__.values():
            add_arg(parser, dc_field)
    else:
        print(f"Warning: {type(dc)} not dataclass type")  # ? warning ?


def create_dc_obj(dc: Type[Any], args: argparse.Namespace) -> object:
    """create dataclass instance from argparse cfg"""
    if not dataclasses.is_dataclass(dc):
        print(f"Error: {type(dc)} not dataclass type")
        return None  # ? raise error ?
    kwargs = {
        key: val for key, val in args.__dict__.items() if key in dc.__dataclass_fields__
    }
    return dc(**kwargs)


def parse_args(cfg: Type[Any], parser_cfg: Optional[ArgumentParserCfg] = None) -> Any:
    """parse args"""
    parser = create_parser(parser_cfg)
    add_args_from_dc(parser, cfg)
    args = parser.parse_args()
    return create_dc_obj(cfg, args)


def field_argument(
    *name_or_flags: str,
    default: Any = MISSING,
    default_factory: Any = MISSING,
    init: bool = True,
    repr: bool = True,  # pylint: disable=redefined-builtin
    hash: Optional[bool] = None,  # pylint: disable=redefined-builtin
    compare: bool = True,
    metadata: Optional[Mapping[Any, Any]] = None,
    kw_only: bool = MISSING,  # type: ignore
    flag: Optional[str] = None,
    action: Optional[str] = None,
    nargs: Optional[int] = None,
    const: Optional[str] = None,
    type: Union[  # pylint: disable=redefined-builtin
        str, argparse.FileType, None
    ] = None,
    choices: Optional[Iterable[Any]] = None,
    required: Optional[bool] = None,
    help: Optional[str] = None,  # pylint: disable=redefined-builtin
    metavar: Optional[str] = None,
    dest: Optional[str] = None,
    version: Optional[str] = None,  # pylint: disable=unused-argument
) -> Any:
    """Return an object to identify dataclass fields with arguments for argparse.
    Wrapper over dataclasses.field.

    default is the default value of the field.  default_factory is a
    0-argument function called to initialize a field's value.  If init
    is true, the field will be a parameter to the class's __init__()
    function.  If repr is true, the field will be included in the
    object's repr().  If hash is true, the field will be included in the
    object's hash().  If compare is true, the field will be used in
    comparison functions.  metadata, if specified, must be a mapping
    which is stored but not otherwise examined by dataclass.  If kw_only
    is true, the field will become a keyword-only parameter to
    __init__().

    It is an error to specify both default and default_factory.
    """

    arg_metadata = add_argument_metadata(
        *name_or_flags,
        flag=flag,
        action=action,
        nargs=nargs,
        const=const,
        type=type,
        choices=choices,
        required=required,
        help=help,
        metavar=metavar,
        dest=dest,
        # version=version,
    )
    field_kwargs = {
        "default": default,
        "default_factory": default_factory,
        "init": init,
        "repr": repr,
        "hash": hash,
        "compare": compare,
    }
    if sys.version_info.minor >= 10:  # from python 3.10  # pragma: no cover
        field_kwargs["kw_only"] = kw_only

    if metadata is not None:
        arg_metadata.update(metadata)
    field_kwargs["metadata"] = arg_metadata

    return Field(**field_kwargs)  # type: ignore
