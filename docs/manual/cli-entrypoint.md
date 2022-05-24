# Building CLI

We are going to build a simple CLI app in this tutorial. We called it `awesome`.

First, let's define our project structure:

```console
$ mkdir awesome
$ touch awesome/awesome
```

Create the storages:

```console
$ mkdir -p storage_X/cli/dev
$ mkdir -p storage_Y/cli/dev
```

Now we will define our CLI entrypoint as:

```py
#!/usr/bin/env python3

"""
DynaCLI bootstrap script # Change me
"""


import os
import sys
from typing import Final

from dynacli import main

cwd = os.path.dirname(os.path.realpath(__file__))

__version__: Final[str] = "1.0.0"

search_path = [f'{cwd}/storage_X/cli/dev', f'{cwd}/storage_Y/cli/dev']
sys.path.extend(search_path)

# root_packages = ['cli.dev', 'cli.admin'] # Change me if you have predefined root package name
# main(search_path, root_packages) # Uncomment if you have root_packages defined

main(search_path)
```

If you wonder what is this `search_path`, please refer to the [Search Path manipulation](../advanced/search-path.md) section of the Advanced Reference Manual.

The next is to start adding packages as features.
