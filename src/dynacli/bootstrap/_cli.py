#!/usr/bin/env python3

"""
DynaCLI bootstrap script
"""

import os
import sys

cwd = os.path.dirname(os.path.realpath(__file__))

search_path = [cwd]
sys.path.extend(search_path)

from dynacli import main as dynamain


def main():
    dynamain(search_path)


if __name__ == "__main__":
    main()
