"""
Convert your Python functions into CLI commands
"""
import re
import sys
from argparse import Action, ArgumentParser
from enum import Enum, EnumMeta
from functools import partial
from importlib import import_module
from inspect import Parameter, signature
from itertools import product
from os import path
from pkgutil import iter_modules
from types import MappingProxyType, ModuleType
from typing import (
    Any,
    AnyStr,
    Callable,
    Final,
    Iterator,
    Match,
    Optional,
    Pattern,
    Type,
    TypedDict,
    Union,
)

# This is for indicating the version of our CLI

__version__: Final[str] = "1.0.4"


ARG_PATTERN: Final[Pattern[str]] = re.compile(r"\s*(.+)\s+\(.+\):\s+(.+)$")

ChoicesType = Optional[MappingProxyType[Any, EnumMeta]]


class _KwargsAction(Action):
    """**kwargs argument parsing action"""

    def __call__(self, parser, namespace, values, option_string=None):  # type: ignore
        dict_ = dict(values)
        setattr(namespace, self.dest, dict_)


class ArgProps(TypedDict):
    """Argument properties"""

    dest: str
    nargs: Optional[Union[int, str]]
    choices: ChoicesType
    type: Union[type, callable]
    action: Union[str, callable]


def _get_feature_help(module: object) -> str:
    """
    Get the docstring of the imported module
    :param module: the imported module object
    :return: The docstring as string
    """
    return module.__doc__ or "[ERROR] Missing the module docstring"


def _parse_command_doc(command: callable) -> tuple[str, Optional[str]]:
    """
    The function for parsing function docstring
    :param command: the actual function object
    :return: the description and spec from docstring
    """
    if not command.__doc__:
        return "[ERROR] Missing command docstring", None
    description, _, spec = command.__doc__.partition("Args:")
    return description, spec


def _get_command_description(command: callable) -> str:
    description, _ = _parse_command_doc(command)
    return description


def _get_command_help(name: str, module: object) -> str:
    """
    Get the function docstring from imported module object
    :param name: name of the function
    :param module: the imported module object
    :return: the description string
    """
    return _get_command_description(module.__dict__[name])


def _is_package(module: ModuleType) -> bool:
    return module.__file__ and module.__file__.endswith("__init__.py")


def _is_module_shortcut(name: str, package: ModuleType) -> bool:
    return (
        name in package.__dict__
        and not _is_package(package.__dict__[name])
        and _is_feature_module(name, package.__dict__[name])
    )


def _is_feature_module(name: str, module: ModuleType) -> bool:
    return name not in module.__dict__


def _is_command(name: str, module: ModuleType) -> bool:
    return not (_is_package(module) or _is_feature_module(name, module))


def _is_public(name: str) -> bool:
    return not name.startswith("_")


def _is_callable(command: object) -> bool:
    return isinstance(command, Callable)


def _is_package_command(name: str, package: ModuleType) -> bool:
    return name in package.__dict__ and _is_callable(package.__dict__[name])


def _get_module_help(name: str, module: ModuleType) -> str:
    return (
        _get_command_help(name, module)
        if _is_command(name, module)
        else _get_feature_help(module)
    )


def _execute_command(args: dict[str, ...], func_: callable) -> None:
    """
    Here we are running actual function with positional arguments.
    If the function signature has **kwargs we will get keyword arguments
    and pass to the function accordingly.
    :param args: argument dictionary from argparse
    :param func_: function object to be called
    :return:
    """
    pos_values_ = args.get("pos_args", [])
    kwargs_ = args.get("kwargs")
    func_(*pos_values_, **kwargs_) if kwargs_ else func_(*pos_values_)


def _process_type(type_: type) -> tuple[Union[type, callable], ChoicesType]:
    """
    Function for processing int, str, float, bool and Enum type.
    Currently, we are supporting only these types.
    :param type_: the type name.
    :return: return the tuple of the types.
    """
    try:
        if type_ in {int, str, float, bool}:
            return type_, None
        elif issubclass(type_, Enum):
            return str, getattr(type_, "__members__", {})
    except TypeError:  # Python quirks with Optional etc.gg
        pass
    raise ValueError(f"Unsupported argument type {type_}")


def _calc_n_kwargs(args: list[str]) -> Union[str, int]:
    """
    Here we try to calculate the nargs for **kwargs arguments.
    Basically we are starting from the end until not encountering
    the "=" sign in the provided argument.
    Example: <CLI> <feature> <command> [arguments: pos[bst labs] *args[lib1 lib2] **kwargs[name1=lib1 name2=lib2]]
    :param args: the list of arguments from the argparse
    :return: nargs for argparse add_argument()
    """
    n_kwargs = 0
    for n_kwargs in range(0, -len(args), -1):
        if "=" not in args[n_kwargs - 1]:
            break
    return -n_kwargs or "*"


def _get_kwargs_arg_props(
    param_type: type, args: list[str], nargs: Union[str, int, None]
) -> ArgProps:
    """
    The function for calculating the nargs of argparse.add_argument();
    We will use it for understanding the count of the CLI arguments,
    and getting them as keyword arguments(**kwargs).
    :param param_type: the argument type
    :param args: list of the arguments from CLI
    :param nargs: the previous nargs to check if **kwargs was preceded by *args or not
    :return:
    """
    # If previous nargs is None it means there is no *args at function signature,
    # and we can return "*" for nargs;
    # of the **kwargs. example: def func_(a: int, b: str, **kwargs: str)

    _, choices = _process_type(param_type)
    nargs = _calc_n_kwargs(args) if nargs == "*" else "*"

    def _process_value(value: str) -> tuple[str, type]:
        name, _, val = value.partition("=")
        return name, param_type(val)

    return ArgProps(
        type=_process_value,
        choices=choices,
        nargs=nargs,
        action=_KwargsAction,
        dest="kwargs",
    )


def _get_regular_arg_props(
    param_type: type,
    _1: list[str],
    _2: Optional[Union[str, int]],
    nargs: Optional[str],
    action: str,
    dest: str,
) -> ArgProps:
    """
    Function for processing regular arguments(positional and *args)
    :param param_type: Parameter type
    :param _1: the list of arguments from argparse (ignored)
    :param _2: previous nargs (ignored)
    :param nargs: new nargs
    :param action: for add_argument()
    :param dest: for add_argument()
    :return:
    """
    arg_type, choices = _process_type(param_type)
    return ArgProps(
        type=arg_type, choices=choices, nargs=nargs, action=action, dest=dest
    )


_PARAM_KIND_MAP: Final[dict[str, callable]] = {
    "VAR_POSITIONAL": partial(
        _get_regular_arg_props, nargs="*", action="extend", dest="pos_args"
    ),
    "VAR_KEYWORD": _get_kwargs_arg_props,
    "POSITIONAL_OR_KEYWORD": partial(
        _get_regular_arg_props, nargs=None, action="append", dest="pos_args"
    ),
}


def _make_arg_help(
    arg_name: str, param_docs: Optional[dict[str, str]], choices: ChoicesType
):
    arg_help = (
        param_docs.get(
            arg_name,
            "[ERROR] Missing argument docstring or the name in the docstring mismatches",
        )
        if param_docs
        else "[ERROR] Docstring format seems to be incorrect or is completely missing"
    )
    if choices:
        arg_help += f" {list(choices)}"
    return arg_help


def _make_arg_metavar(arg_name: str, arg_dest: str) -> str:
    if arg_dest == "kwargs":
        arg_name += " <name>=<value>"

    return arg_name


def _add_command_arg(
    parser: ArgumentParser,
    arg_name: str,
    param: Parameter,
    param_docs: Optional[dict[str, str]],
    args: list[str],
    nargs: Union[str, int, None],
) -> Union[str, int, None]:
    """
    Here we are converting function arguments from the signature to CLI argument.
    I.E each function argument is a separate CLI argument.
    Example: def poll(name: str, age: int, *args, **kwargs) -
    that means poll command expects name and age as positional CLI arguments,
    if passed *args and **kwargs will be treated accordingly.
    :param parser: parser object from argparse
    :param arg_name: actual argument name from the function signature
    :param param: actual Parameter from the function signature
    :param param_docs: the dict of argument_name: help message parsed from the docstring
    :param args: list of command line arguments
    :param nargs: previous nargs for checking *args, **kwargs order
    :return:
    """
    arg_props = _PARAM_KIND_MAP[param.kind.name](param.annotation, args, nargs)
    arg_help = _make_arg_help(arg_name, param_docs, arg_props["choices"])
    arg_metavar = _make_arg_metavar(arg_name, arg_props["dest"])
    parser.add_argument(
        **arg_props,
        help=arg_help,
        metavar=arg_metavar,
    )
    return arg_props["nargs"]


def _convert_docstring_to_param_docs(params: Optional[list[str]]) -> dict[str, str]:
    """
    Here we are converting the docstring arguments of the function to the dictionary.
    :param params: The list of arguments from the docstring of the function
    :return:
    """
    param_docs: dict[str, str] = {}
    if params is not None and [""] != params:
        _build_param_docs(params, param_docs)
    return param_docs


def _build_param_docs(params: list[str], param_docs: dict[str, str]) -> None:
    """
    Build parameters documentation dictionary
    :param params: list of docstrings from function specification
    :param param_docs: resulting dictionary
    """
    for arg in params:
        match_ = ARG_PATTERN.match(arg)
        if not match_:
            break
        _add_param_doc(param_docs, match_)


def _add_param_doc(param_docs: dict[str, str], match: Match[AnyStr]) -> None:
    """
    Insert one parameter documentation into dictionary
    :param param_docs: resulting dictionary
    :param match: outcome of the regular expression matching
    """
    param_name = str(match[1]).lstrip("*")
    param_doc = str(match[2])
    param_docs[param_name] = param_doc


def _add_version(parser: ArgumentParser, module: ModuleType) -> None:
    """
    Implementing --version argument if there is a __version__ defined in the module(package)
    :param parser: parser object from the argparse
    :param module: actual imported module
    :return:
    """
    version_ = _get_version(module)
    if version_:
        parser.add_argument(
            "-v", "--version", action="version", version="%(prog)s - v" + version_
        )


def _get_args_from_spec(spec: Optional[str]) -> Optional[list[str]]:
    if not spec:
        return None
    args_spec, _, _ = spec.partition("Return:")
    return args_spec.strip().split("\n")


def _get_python_name(iter_: Iterator) -> str:
    return next(iter_).replace("-", "_")


def _get_cli_name(name: str) -> str:
    return name.replace("_", "-")


def _get_all__(module: ModuleType) -> list[str]:
    return module.__dict__.get("__all__", [])


def _get_version(module: ModuleType) -> Optional[str]:
    return module.__dict__.get("__version__")


def _get_root_description() -> tuple[Optional[str], ModuleType]:
    main_module = sys.modules["__main__"]
    return main_module.__doc__, main_module


class _ArgParsingContext:
    def __init__(
        self,
        root_packages: Optional[list[str]],
        search_path: list[str],
        args: list[str],
    ) -> None:
        self._root_packages = (
            [r if r.endswith(".") else r + "." for r in root_packages]
            if root_packages
            else [""]
        )
        self._search_path = [p if p.endswith("/") else p + "/" for p in search_path]
        self._args = args
        self._root_parser: ArgumentParser = None  # type: ignore
        self._current_subparsers: ArgumentParser._Subparsers = []  # type: ignore
        self._current_package: ModuleType = None  # type: ignore
        self._current_command = None
        self._known_names: set[str] = set()

    def set_root_parser(self, arg: str) -> None:
        description, main_module = _get_root_description()
        self._root_parser = ArgumentParser(
            prog=path.basename(arg),
            description=description,
        )
        self._current_subparsers = self._root_parser.add_subparsers()
        _add_version(self._root_parser, main_module)

    def _set_known_names(self):
        for name, module in self._current_package.__dict__.items():
            if _is_public(name) and (
                _is_callable(module) or _is_module_shortcut(name, self._current_package)
            ):
                self._known_names.add(name)

    def _add_known_functions(self):
        for name in self._known_names:
            module = self._current_package.__dict__[name]
            if _is_callable(module):
                self.add_command_parser(name, self._current_package)

    def _add_known_modules(self):
        for name in self._known_names:
            module = self._current_package.__dict__[name]
            if not _is_callable(module) and _is_module_shortcut(
                name, self._current_package
            ):
                self.add_feature_parser(name, module)

    def build_all_features_help(self) -> None:
        """
        Here we are iterating through the search path and registering all features.
        Effectively is equal to: <CLI> -h run
        :return:
        """

        self._add_parsers(
            [
                (path_ + root_.replace(".", "/"))[:-1]
                for root_, path_ in product(self._root_packages, self._search_path)
            ]
        )

    def build_feature_help(self) -> None:
        self._set_known_names()
        self.build_all_features_help()
        # You may argue about repeated for loops; the issue is that the order of function and module additions to the argparse matters;
        self._add_known_functions()
        self._add_known_modules()

    def build_features_help_with_all_(self, module: ModuleType) -> None:
        """
        Same as build_all_features_help,
        except we are not scanning the search path but only __all__ if specified
        :param module: actual imported module
        :return:
        """
        for name_ in _get_all__(module):
            if _is_public(name_):
                self._add_parser(name_)

    def execute(self) -> None:
        """
        This is for actual execution of our CLI command - for Python this is an actual function call
        :return:
        """
        args = vars(self._root_parser.parse_args())
        if not args and not self._current_command:
            self._root_parser.print_usage()
            sys.exit(1)
        _execute_command(args, self._current_command)

    def import_module(self, name) -> ModuleType:
        err_msg = None
        for package in self._root_packages:
            full_name = package + name
            try:
                return import_module(full_name)
            except ImportError as err:
                if f"No module named '{full_name}'" != err.msg:
                    err_msg = err.msg
                    break
            except Exception as err:
                err_msg = str(err)
                break

        raise ImportError(f"{name} - {err_msg}")

    def add_feature_parser(self, name: str, module: ModuleType) -> None:
        self._root_packages = [module.__name__ + "."]
        parser = self._current_subparsers.add_parser(
            _get_cli_name(name), help=_get_feature_help(module)
        )
        self._current_subparsers = parser.add_subparsers()
        _add_version(parser, module)

    def add_feature(self, name: str, module: ModuleType) -> None:
        self.add_feature_parser(_get_cli_name(name), module)
        self._current_package = module
        f_name = module.__file__ or ""
        self._search_path = [p for p in self._search_path if f_name.startswith(p)]

    def add_command_parser(self, name: str, module: ModuleType) -> None:
        command = module.__dict__[name]
        description, spec = _parse_command_doc(command)
        arg_docs = _convert_docstring_to_param_docs(_get_args_from_spec(spec))
        parser = self._build_command_executor(
            command, _get_cli_name(name), description, arg_docs
        )
        _add_version(parser, module)
        return None

    def build_module_feature_help(self, module: ModuleType) -> None:
        """
        Here we are registering module as feature functions as subparsers(i.e as commands);
        by scanning the module dictionary.
        :param module: imported module
        :return:
        """
        for name, command in module.__dict__.items():
            if _is_public(name) and _is_callable(command):
                self._current_subparsers.add_parser(
                    name, help=_get_command_description(command)
                )

    def build_module_feature_help_with_all_(self, module: ModuleType) -> None:
        """
        Same as build_module_feature_help, except we are scanning __all__ if it is defined.
        :param module: import module
        :return:
        """
        for name_ in _get_all__(module):
            self._current_subparsers.add_parser(
                name_, help=_get_command_description(command=module.__dict__[name_])
            )

    def _add_parsers(self, paths_: list[str]) -> None:
        for module_info in sorted(iter_modules(paths_), key=lambda m: m.name):
            name = module_info.name
            if _is_public(name) and name not in self._known_names:
                self._add_parser(name)

    def _add_parser(self, name: str) -> None:
        try:
            module = self.import_module(name)
            help_ = _get_module_help(name, module)
        except ImportError as err:
            help_ = "[ERROR] failed to import " + err.msg
        finally:
            self._current_subparsers.add_parser(_get_cli_name(name), help=help_)

    def _build_command_executor(
        self,
        command: callable,
        name: str,
        description: str,
        param_docs: Optional[dict[str, str]],
    ) -> ArgumentParser:
        """
        Here we build complete command executor functionality -
        I.E registering each argument of the function;
        as CLI argument of the command
        :param command: the function object
        :param name: the command name to register as subparser
        :param description: help description of the command
        :param param_docs: arguments dictionary with help messages
        :return: parser object
        """
        parser = self._current_subparsers.add_parser(name, help=description)
        sig_ = signature(command)
        self._current_command = command
        nargs = None
        try:
            for arg_name, param in sig_.parameters.items():
                nargs = _add_command_arg(
                    parser, arg_name, param, param_docs, self._args, nargs
                )
        except ValueError as err:
            parser.error(str(err))
        return parser


# ArgParsing State Machine controlling gradual progress;
# from the cli script name to command via intermediate features

_ArgParsingState = Optional[
    Callable[[Iterator[str], _ArgParsingContext], Optional[Type["_ArgParsingState"]]]
]


def _waiting_for_feature_module_command(module: ModuleType) -> _ArgParsingState:
    def _check_feature_module_command(
        iter_: Iterator[str], context: _ArgParsingContext
    ) -> None:
        try:
            context.add_command_parser(_get_python_name(iter_), module)
            return None
        except (StopIteration, KeyError):
            context.build_module_feature_help(module)

    return _check_feature_module_command


def _waiting_for_feature_module_all_(module: ModuleType) -> _ArgParsingState:
    def _check_feature_module_command_all_(
        iter_: Iterator[str], context: _ArgParsingContext
    ) -> None:
        try:
            name = _get_python_name(iter_)
            if name in _get_all__(module):
                context.add_command_parser(name, module)
                return None
        except (StopIteration, KeyError):
            pass
        context.build_module_feature_help_with_all_(module)
        return None

    return _check_feature_module_command_all_


def _waiting_for_feature_package_all_(module: ModuleType) -> _ArgParsingState:
    def _check_feature_all_(
        iter_: Iterator[str], context: _ArgParsingContext
    ) -> Optional[_ArgParsingState]:
        try:
            name = _get_python_name(iter_)
            module_ = context.import_module(name)
            if name in _get_all__(module):
                return _choose_state(context, module_, name)
        except (StopIteration, ImportError):
            pass
        context.build_features_help_with_all_(module)
        return None

    return _check_feature_all_


def _waiting_for_all_(
    name: str, module: ModuleType, context: _ArgParsingContext
) -> _ArgParsingState:
    if _is_package(module):
        context.add_feature(name, module)
        return _waiting_for_feature_package_all_(module)
    else:
        context.add_feature_parser(name, module)
        return _waiting_for_feature_module_all_(module)


def _waiting_for_first_feature_or_command(
    iter_: Iterator[str], context: _ArgParsingContext
) -> Optional[_ArgParsingState]:
    try:
        name = _get_python_name(iter_)
        module = context.import_module(name)
        return _choose_state(context, module, name)
    except (StopIteration, ImportError):
        context.build_all_features_help()
        return None


def _waiting_for_nested_feature_or_command(
    iter_: Iterator[str], context: _ArgParsingContext
) -> Optional[_ArgParsingState]:
    try:
        name = _get_python_name(iter_)
        curr_package = context._current_package
        if _is_package_command(name, curr_package):
            context.add_command_parser(name, curr_package)
            return
        if _is_module_shortcut(name, curr_package):
            module_ = curr_package.__dict__[name]
            context.add_feature_parser(name, module_)
            return _waiting_for_feature_module_command(module_)
        module = context.import_module(name)
        return _choose_state(context, module, name)
    except (StopIteration, ImportError):
        context.build_feature_help()
        return None


def _choose_state(
    context: _ArgParsingContext, module: ModuleType, name: str
) -> Optional[_ArgParsingState]:
    try:
        if "__all__" in module.__dict__:
            return _waiting_for_all_(name, module, context)
        elif _is_package(module):
            context.add_feature(name, module)
            return _waiting_for_nested_feature_or_command
        elif _is_feature_module(name, module):
            context.add_feature_parser(name, module)
            return _waiting_for_feature_module_command(module)
        else:
            context.add_command_parser(name, module)
            return None
    except (StopIteration, ImportError, KeyError):
        context.build_all_features_help()
        return None


def _initial_state(
    iter_: Iterator[str], context: _ArgParsingContext
) -> _ArgParsingState:
    context.set_root_parser(next(iter_))
    return _waiting_for_first_feature_or_command


def main(
    search_path: list[str],
    root_packages: Optional[list[str]] = None,
) -> None:
    """
    This is the main entrypoint for the CLI.
    :param search_path: the list of paths to look for features
    :param root_packages: (optional) the list of root package names
    :return:
    """
    args = [arg for arg in sys.argv if arg not in {"-h", "--help", "-v", "--version"}]
    iter_ = iter(args)
    context = _ArgParsingContext(root_packages, search_path, args)
    current_state = _initial_state
    while current_state is not None:
        current_state = current_state(iter_, context)
    context.execute()


__all__: Final[list[callable]] = ["main", "__version__"]
