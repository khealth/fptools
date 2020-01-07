import sys
from dataclasses import asdict
from .docs import get_documentation, dump_documentation

if __name__ == "__main__":
    module_name = sys.argv[1]

    if len(sys.argv) < 2:
        sys.stderr.write("Not enough arguments.\n")
        sys.stderr.write("python -m documentation_generator [module]\n")
        exit(1)

    documentation = get_documentation(module_name)
    dump_documentation(documentation, sys.stdout)
