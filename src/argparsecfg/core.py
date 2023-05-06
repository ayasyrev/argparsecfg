from __future__ import annotations

import argparse
import dataclasses
import sys
from argparse import HelpFormatter
from dataclasses import MISSING, Field, asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple, Type, Union

_MISSING_TYPE = type(MISSING)


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


@dataclass
class ArgCfg:
    """args container for parser.add_argument.
    first draft.
    """

    # *name_or_flags: str,
    flag: Optional[str]  # use it for "short" flag
    action: Optional[str]  # _ActionStr | Type[Action] = ...,
    nargs: Optional[int]  # | _NArgsStr | _SUPPRESS_T = ...,
    const: Optional[str]  # Any = ...,
    default: Optional[str]  # Any = ...,
    type: Union[
        str, argparse.FileType, None
    ]  # ((str) -> _T@add_argument) | FileType = ...,
    choices: Optional[Iterable[Any]]  # Iterable[_T@add_argument] | None = ...,
    required: bool  # = ...,
    help: Optional[str]  # | None  = ...,
    metavar: Union[str, Tuple[str, ...], None]  # | tuple[str, ...] | None = ...,
    dest: Optional[str]  # | None = ...,
    # version: Optional[str]  # = ...,


def add_argument_metadata(
    flag: Optional[str] = None,  # simple ver, check if "name", list of flags
    *,
    action: Optional[str] = None,  # _ActionStr | Type[Action] = ...,
    nargs: Optional[int] = None,  # | _NArgsStr | _SUPPRESS_T = ...,
    const: Optional[str] = None,  # Any = ...,
    # default set at dataclass field, check type!
    default: Optional[Any] = None,  # Any = ...,
    # ! set type at dataclass field! check! ((str) -> _T@add_argument) | FileType = ...,
    type: Union[  # pylint: disable=redefined-builtin
        str, argparse.FileType, None
    ] = None,
    # check choices type! Iterable[_T@add_argument] | None = ...,
    choices: Optional[Iterable[Any]] = None,
    required: bool = False,  # = ...,
    help: Optional[str] = None,  # pylint: disable=redefined-builtin
    metavar: Union[str, Tuple[str, ...], None] = None,  # |  = ...,
    dest: Optional[str] = None,
    version: Optional[str] = None,  # pylint: disable=unused-argument  # not implemented
) -> Dict[str, Any]:
    """create dict with args for argparse.add_argument"""
    return asdict(
        ArgCfg(
            flag=flag,
            action=action,
            nargs=nargs,
            const=const,
            default=default,
            type=type,
            choices=choices,
            required=required,
            help=help,
            metavar=metavar,
            dest=dest,
            # version=version,
        )
    )


def parse_metadata(
    metadata: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        key: val
        for key, val in metadata.items()
        if key in ArgCfg.__dataclass_fields__  # pylint: disable=no-member
    }


def add_arg(parser: argparse.ArgumentParser, dc_field: Field[Any]) -> None:
    """add argument to parser from dataclass field"""
    flags = [f"{parser.prefix_chars * 2}{dc_field.name}"]
    if dc_field.metadata:
        kwargs = parse_metadata(dc_field.metadata)
        flag = kwargs.pop("flag", None)
        if flag is not None:
            if flag == "POSITIONAL_ARGUMENT":
                flags = [kwargs.pop("dest")]
                kwargs.pop("required")
                # positional_arg = True
            else:
                # todo check flag correct
                flags.insert(
                    0,
                    flag
                    if flag.startswith(parser.prefix_chars)
                    else f"{parser.prefix_chars}{flag}"
                )
    else:
        kwargs: dict[str, Any] = {}
    # check values from metadata - default & type
    metadata_type = kwargs.pop("type", None)
    metadata_default = kwargs.pop("default", None)
    kwargs["type"] = get_field_type(dc_field)
    if metadata_type is not None:
        if kwargs["type"] != metadata_type:
            # ? assert
            print(
                f"Warning: arg {dc_field.name} type is {kwargs['type']} but at metadata {metadata_type}"
            )
    if isinstance(dc_field.default, _MISSING_TYPE):
        default = None
    else:
        default = dc_field.default
        kwargs["default"] = default

    if dc_field.metadata and metadata_default:  # check only if metadata
        if not isinstance(default, type(metadata_default)):
            default_type = type(default)
            metadata_default_type = type(metadata_default)
            print(
                f"Warning: default_type={default_type}, metadata_default_type={metadata_default_type}"
            )
        if default != metadata_default:
            print(f"Warning: default={default}, metadata_default={metadata_default}")

    # if default is None:
    #     kwargs["required"] = True
    # else:
    # if positional_arg:
    #     kwargs.pop("required", None)

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
    *args: str,
    # *,
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
    required: bool = False,
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
    if args:
        if len(args) == 1:
            if args[0][0] == "-":
                flag = args[0]
            else:
                dest = args[0]  # ?disable flag
                flag = "POSITIONAL_ARGUMENT"  # for disable later
        else:
            if len(args) == 2:
                flag = args[0]  # expecting short flag first
                dest = args[1]
                if dest.startswith("--"):
                    dest = dest[2:]
            else:
                raise ValueError("Invalid number of arguments")

    arg_metadata = add_argument_metadata(
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

    if default is not MISSING and default_factory is not MISSING:  # pragma: no cover
        raise ValueError("cannot specify both default and default_factory")

    return Field(**field_kwargs)
