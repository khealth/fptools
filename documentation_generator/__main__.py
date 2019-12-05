import sys
import importlib
import json
from dataclasses import asdict
from .docs import get_documentation

if len(sys.argv) < 2:
    sys.stderr.write("Not enough arguments.\n")
    sys.stderr.write("python -m documentation_generator [module]\n")
    exit(1)

module_name = sys.argv[1]

module = importlib.import_module(module_name)
documentation = get_documentation(module) # mypy: ignore

json.dump(asdict(documentation), sys.stdout, indent=4)