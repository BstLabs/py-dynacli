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

You can use `dynacli init <CLI name> path=<actual path>` command for bootstrapping the entry point file:

```bash
$ cd tutorials/greetings

$ dynacli init say path=.
Successfully created CLI entrypoint say at /home/ssm-user/OSS/py-dynacli/tutorials/greetings
```

The created `say` file has some comments to change accordingly:

```python
#!/usr/bin/env python3

"""
DynaCLI bootstrap script # Change me
"""


import os
import sys
from typing import Final

from dynacli import main

cwd = os.path.dirname(os.path.realpath(__file__))

__version__: Final[str] = "0.0.0" # Change me to define your own version


search_path = [cwd] # Change me if you have different path; you can add multiple search pathes
sys.path.extend(search_path)
# root_packages = ['cli.dev', 'cli.admin'] # Change me if you have predefined root package name
# main(search_path, root_packages) # Uncomment if you have root_packages defined

main(search_path)

```

Let's change it:

```python
#!/usr/bin/env python3
"""
Greetings CLI
"""

import sys
import os
from typing import Final

from dynacli import main

cwd = os.path.dirname(os.path.realpath(__file__))

__version__: Final[str] = "1.0"

search_path = [cwd]
sys.path.extend(search_path)

main(search_path)
```

That is it, now we have ready to go CLI.

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

Let's get the help message:

```bash
$ ./say -h
usage: say [-h] [-v] {hello} ...

Greetings CLI

positional arguments:
  {hello}
    hello        Print Hello <first-name> <last-name> message

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

We can get the version as easy as:

```bash
$ ./say --version
say - v1.0
```

Now the help about actual command:

```bash
$ ./say hello -h
usage: say hello [-h] [names ...]

positional arguments:
  names       variable list of names to be included in greeting

optional arguments:
  -h, --help  show this help message and exit
```

Finally we can run the actual command(the hello function in fact) as:

```bash
$ ./say hello Shako Rzayev Asher Sterkin
Hello, Shako Rzayev Asher Sterkin
```

Go to [tutorials/greetings](tutorials/greetings) folder and try it yourself.

## Read the full documentation

[DynaCLI Github Pages](https://bstlabs.github.io/py-dynacli/)


## License

MIT License, Copyright (c) 2021-2022 BST LABS. See [LICENSE](LICENSE.md) file.
