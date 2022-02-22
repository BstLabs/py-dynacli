#!/usr/bin/env python3

"""
DynaCLI bootstrap script
"""

import os
import sys

from dynacli import main as dynamain

cwd = os.path.dirname(os.path.realpath(__file__))

search_path = [cwd]
sys.path.extend(search_path)


# For package distro purposes
def main():
    dynamain(search_path)


if __name__ == "__main__":
    main()
