# DynaCLI

DynaCLI (Dynamic CLI) is a cloud-friendly Python library for converting pure Python functions into Linux Shell commands on the fly.

It's ideal for automating routine development and administrative tasks in a modern cloud software environment because it supports converting a virtually unlimited set of functions into Shell commands with minimal run-time and maintenance overhead.

Unlike other existing solutions such as [Click](https://click.palletsprojects.com/en/8.0.x/) and [Typer](https://typer.tiangolo.com/), there is no need for any function decorators. Further, unlike with all existing solutions, including those built on top of standard [argparse](https://docs.python.org/3/library/argparse.html), DynaCLI does not build all command parsers upfront, but rather builds dynamically a single command parser based on the command line inputs. When combined with the [Python Cloud Importer](https://asher-sterkin.medium.com/serverless-cloud-import-system-760d3c4a60b9) solution, DynaCLI becomes truly _open_ with regard to a practically unlimited set of commands, all coming directly from cloud storage. This, in turn, eliminates any need for periodic updates on client workstations.

At its core, DynaCLI is a Python package structure interpreter which makes any public function executable from the command line.

DynaCLI was developed by BST LABS as an open source generic infrastructure foundation for the cloud version of Python run-time within the scope of the [Cloud AI Operating System (CAIOS)](http://caios.io) project.

For details about the DynaCLI rationale and design considerations, refer to [DynaCLI Github Pages](https://bstlabs.github.io/py-dynacli/).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install DynaCLI from the PyPi site:

```bash
pip3 install dynacli
```

## Usage

## Define command line interpreter entry point

```python
#!/usr/bin/env python3
"""
Greetings CLI
"""

import sys
import os
from dynacli import main

# Yes you can define your own version here
__version__ = "1.0"

cwd = os.path.dirname(__file__)
# The list of the paths for searching packages and modules by DynaCLI
# This is a simplest possible configuration. Look at [TBD]() for complete list
# of configuration options and typical use cases for each one.
search_path = [f'{cwd}/<path-to-cli-functions>']
# This needs to be done only if your sys.path does not already include it 
sys.path.extend(search_path)

main(search_path)
```

## Define commands

Every public function in your search path will be treated as a command. For example,

```python
def hello(*names: str) -> None:
    """
    Print Hello <first-name> <last-name> message
    
    Args:
        names (str): variable list of names to be included in greeting
        
    Return: None
    """
    print(f"Hello, {' '.join(names)}")
```

## Start using CLI

Just type your command line interpreter entry point script followed by command name and arguments, if any. For example:

```bash
./say hello World! 
```

Go to [tutorials/greetings](tutorials/greetings) folder and try it yourself.

## Read the full documentation

[DynaCLI Github Pages](https://bstlabs.github.io/py-dynacli/)

## Project layout

```bash
    py-dynacli/
    ├── docs                # (1) 
    │   └── tutorial
    ├── scripts             # (2)
    ├── tutorials           # (3)
    ├── src                 # (4) 
    │   └── python
    └── test                # (5) 
        └── integrated
            ├── storage_X
            │   └── cli
            │       ├── admin
            │       │   └── feature_C
            │       └── dev
            │           └── feature_A
            ├── storage_Y
            │   └── cli
            │       ├── admin
            │       │   └── feature_D
            │       └── dev
            │           └── feature_B
            └── suite
```

1. The documentation files
2. Helper bash scripts
3. Tutorials
4. The main source folder
5. Here we have tests

## License

MIT License, Copyright (c) 2021-2022 BST LABS. See [LICENSE](LICENSE.md) file.
