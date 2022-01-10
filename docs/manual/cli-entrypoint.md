# Building CLI

We are going to build simple CLI app in this tutorial. We called it `awesome`.

First let's define our project structure:

```bash
$ mkdir awesome
$ touch awesome/awesome
```

Create the storages:

```bash
$ mkdir -p storage_X/cli/dev
$ mkdir -p storage_Y/cli/dev
```

Now we will define our CLI entrypoint as:

```py
#!/usr/bin/env python3
import sys
import os
from dynacli import main

cwd = os.path.dirname(__file__)

search_path = [f'{cwd}/storage_X/cli/dev', f'{cwd}/storage_Y/cli/dev']
sys.path.extend(search_path)

main(search_path)
```

If you wonder what is this `search_path`, please refer to [DynaCLI is cloud friendly](../advanced/search-path.md) section of Advanced Reference Manual.

The next is to start adding package as features.
