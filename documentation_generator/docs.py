import inspect
from types import ModuleType
from dataclasses import dataclass, field
import pkgutil
from typing import List, Generator, TypeVar, ClassVar


@dataclass
class Doc:
    type: str = field(init=False, default="object")
    name: str
    doc: str


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


def get_doc(name: str, obj) -> Doc:
    doc = inspect.getdoc(obj)
    if inspect.isfunction(obj):
        return FunctionDoc(name, doc, signature=repr(inspect.signature(obj)))

    return Doc(name, doc)


def get_documentation(module: ModuleType) -> ModuleDoc:
    is_pkg = is_package(module)

    member_docs = [
        get_doc(name, member)
        for name, member
        in get_module_members(module)
        if not isinstance(member, TypeVar) and not name.startswith('_')
    ]

    if is_pkg:
        submodule_docs = [
            get_documentation(submodule)
            for submodule
            in iter_submodules(module)
        ]
        member_docs = submodule_docs + member_docs

    return ModuleDoc(
        name=module.__name__,
        doc=inspect.getdoc(module),
        file=module.__file__,
        is_pkg=is_pkg,
        members=member_docs,
    )


def iter_submodules(module: ModuleType) -> Generator[ModuleType, None, None]:
    """
    Iterate through all submodules of given module
    """
    submodule_names = [
        modname
        for importer, modname, ispkg
        in pkgutil.iter_modules(module.__path__)
    ]
    with_submodules = __import__(module.__name__, fromlist=submodule_names)
    for name in submodule_names:
        yield getattr(with_submodules, name)


def get_module_members(module: ModuleType):
    """
    Like inspect.get_members() but only returns members defined in module
    """
    return inspect.getmembers(module, lambda item: inspect.getmodule(item) is module)


def is_package(module: ModuleType) -> bool:
    """
    Returns whether a module is a package.
    https://docs.python.org/3/reference/import.html:
    "It’s important to keep in mind that all packages are modules, but not all modules are packages. Or put another way,
    packages are just a special kind of module. Specifically, any module that contains a __path__ attribute is
    considered a package."
    """
    return hasattr(module, "__path__")
