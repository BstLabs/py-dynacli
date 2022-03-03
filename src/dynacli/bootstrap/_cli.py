#!/usr/bin/env python3

"""
DynaCLI bootstrap script
"""

import os
import sys

from dynacli import __version__ as _version
from dynacli import main as dynamain

cwd = os.path.dirname(os.path.realpath(__file__))

search_path = [cwd]
sys.path.extend(search_path)


# This fix is for dynacli entrypoint script; as it has wrapper __main__ we need to add necessary information

_map = {
    "__version__": _version,
    "__doc__": """
DynaCLI bootstrap script
""",
}


def _set_main_attrs(**kwargs):
    _main = sys.modules["__main__"]
    for key, val in kwargs.items():
        setattr(_main, key, val)


# For package distro purposes
def main():
    _set_main_attrs(**_map)
    dynamain(search_path)


if __name__ == "__main__":
    main()
