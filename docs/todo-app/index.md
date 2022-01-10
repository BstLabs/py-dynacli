# TODO app

We use a To-Do app idea from [Build a Command-Line To-Do App With Python and Typer](https://realpython.com/python-typer-cli/)
Of course, we are going to change and omit unneeded sections. The goal is to show how DynaCLI can ease the process of building CLI apps.

Create TODO directory and create todo file:

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

import sys
import os
from dynacli import main

__version__ = "1.0"

cwd = os.path.dirname(__file__)

sys.path.extend([cwd])

main([cwd])
```

And now we have nice help with description and also with the version. 
Basically, we get the CLI help from the docstring, version from `__version__` and there is no need for any callback.

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

The next is to init the Todo project.
