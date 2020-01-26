import importlib
import inspect
import json
import pkgutil
from dataclasses import asdict, dataclass, field
from types import ModuleType
from typing import Generator, List, Optional, TextIO, TypeVar


@dataclass
class Doc:
    type: str = field(init=False, default="object")
    name: str
    doc: Optional[str]


@dataclass
class ModuleDoc(Doc):
    type: str = field(init=False, default="module")
    is_pkg: bool
    members: List[Doc]
    file: str


@dataclass
class FunctionDoc(Doc):
    type: str = field(init=False, default="function")
    signature: str


@dataclass
class ClassDoc(Doc):
    type: str = field(init=False, default="class")
    members: List[Doc]


class _ModuleTypeWithPath(ModuleType):
    __path__: str


def get_documentation(module_name: str) -> ModuleDoc:
    module = importlib.import_module(module_name)
    return _get_documentation_for_module(module)


def dump_documentation(documentation: ModuleDoc, file: TextIO) -> None:
    json.dump(asdict(documentation), file, indent=4)


def _get_documentation_for_module(module) -> ModuleDoc:
    member_docs: List[Doc]
    is_pkg = _is_package(module)

    member_docs = [
        _get_doc(name, member)
        for name, member in _get_module_members(module)
        if not isinstance(member, TypeVar) and _is_public(name)
    ]

    if is_pkg:
        submodule_docs = [
            _get_documentation_for_module(submodule)
            for submodule in _iter_submodules(module)
        ]
        member_docs = [*submodule_docs, *member_docs]

    return ModuleDoc(
        name=module.__name__,
        doc=inspect.getdoc(module),
        file=module.__file__,
        is_pkg=is_pkg,
        members=member_docs,
    )


def _get_doc(name: str, obj) -> Doc:
    doc = inspect.getdoc(obj)

    if inspect.isclass(obj):
        mro = inspect.getmro(obj)[1:]
        mro_cls_members = [
            (name, member) for cls in mro for name, member in inspect.getmembers(cls)
        ]
        cls_members = inspect.getmembers(type(type(obj)))
        mro_members = mro_cls_members + cls_members
        members = [
            Doc(name, None)
            for name, member in inspect.getmembers(obj)
            if (name, member) not in mro_members
            and _is_public(name)
        ]
        return ClassDoc(name, doc, members)

    if callable(obj):
        return FunctionDoc(name, doc, signature=str(inspect.signature(obj)))

    return Doc(name, doc)


def _iter_submodules(
    module: _ModuleTypeWithPath,
) -> Generator[_ModuleTypeWithPath, None, None]:
    """
    Iterate through all submodules of given module
    """
    submodule_names = [
        modname for importer, modname, ispkg in pkgutil.iter_modules(module.__path__)
    ]
    with_submodules = __import__(module.__name__, fromlist=submodule_names)
    for name in submodule_names:
        yield getattr(with_submodules, name)


def _get_module_members(module: ModuleType):
    """
    Like inspect.get_members() but only returns members defined in module
    """
    return inspect.getmembers(module, lambda item: inspect.getmodule(item) is module)


def _is_package(module: ModuleType) -> bool:
    """
    Returns whether a module is a package.
    https://docs.python.org/3/reference/import.html: "It’s important to keep in
    mind that all packages are modules, but not all modules are packages. Or put
    another way, packages are just a special kind of module. Specifically, any
    module that contains a __path__ attribute is considered a package."
    """
    return hasattr(module, "__path__")


def _is_public(name: str) -> bool:
    return not name.startswith("_")
