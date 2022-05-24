# TODO app

We use a To-Do app idea from [Build a Command-Line To-Do App With Python and Typer](https://realpython.com/python-typer-cli/).
Of course, we are going to change and omit unneeded sections. The goal is to show how DynaCLI can ease the process of building CLI apps.

Create the TODO directory and create the todo file:
```console
$ mkdir TODO
$ dynacli init todo path=TODO/
```

```bash
$ tree
.
└── TODO
    └── todo

1 directory, 1 file
```

CLI entrypoint is quite simple without any pre-configuration:

```py title="todo"
#!/usr/bin/env python3

"""
TODO CLI APP
"""

import os
import sys
from typing import Final

from dynacli import main

cwd = os.path.dirname(os.path.realpath(__file__))

__version__: Final[str] = "1.0.0"

search_path = [cwd]
sys.path.extend(search_path)

main(search_path)
```

And now we have nice help with the description and the version.
Essentially, we get the CLI help from the docstring, version from `__version__` and there is no need for any callback.

```console
$ ./todo -h
usage: todo [-h] [-v] {} ...

TODO CLI APP

positional arguments:
  {}

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

```console
$ ./todo --version
todo - v1.0
```

The next step is to initiate the TODO project.
