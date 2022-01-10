# Package as feature

Now it is time to add our package as features:

```console
$ mkdir storage_X/cli/dev/service
$ touch storage_X/cli/dev/service/__init__.py

$ mkdir storage_Y/cli/dev/environment
$ touch storage_Y/cli/dev/environment/__init__.py
```

That's it you can now run your CLI:

```console hl_lines="7 8"
$ ./awesome -h

usage: awesome [-h] {service,environment} ...

positional arguments:
  {service,environment}
    service             [ERROR] Missing the module docstring
    environment         [ERROR] Missing the module docstring

optional arguments:
  -h, --help            show this help message and exit
```

Our packages have no docstrings in it, due to this fact we got an `ERROR` indicating that we are missing the docstrings.

Let's quickly fix this. We are going to add docstrings to the `__init__.py` files.

Open the `#!python storage_X/cli/dev/service/__init__.py` and add following:

`#!python """The service feature to handle our services"""`

Open the `#!python storage_Y/cli/dev/environment/__init__.py` and add following:

`#!python """The environment feature to handle our environments"""`

Now if you rerun the CLI you can see that there are no `ERROR`s:

```console hl_lines="7 8"
$ ./awesome -h

usage: awesome [-h] {service,environment} ...

positional arguments:
  {service,environment}
    service             The service feature to handle our services
    environment         The environment feature to handle our environments

optional arguments:
  -h, --help            show this help message and exit
```

## Feature commands

What kind of operations we want for our service feature? 
Let's imagine that we can create, update and shutdown the services.
That means we need `new.py`, `update.py` and `shutdown.py` files in service package:

```console
$ touch storage_X/cli/dev/service/new.py
$ touch storage_X/cli/dev/service/update.py
$ touch storage_X/cli/dev/service/shutdown.py
```

We consider commands in the package as feature if they have identical named function in it.
In other words, there should be `#!py new()` function in `new.py`, `#!py update()` in `update.py` etc.

So, let's define our functions(feature commands):

```py title="new.py"
def new(name: str, path: str):
    """
    init the new project in given path

    Args:
        name (str): name of the project
        path (str): path where to create service

    Return: None
    """
    print(f"Initializing the {name} in {path}")
```

```py title="update.py"
def update(name: str, version: float, upgrade: bool, *args: str, **kwargs: int) -> None:
    """
    Updates the service...

    Args:
        name (str): name of the service
        version (float): new version
        upgrade (bool): if to upgrade everything
        *args (str): variable length arguments
        **kwargs (int): keyword arguments

    Return: None
    """
    print(f"Updating...{name} to {version} with {upgrade=} using {args} and {kwargs}")
```

```py title="shutdown.py"
def shutdown(environment: str, service: str) -> None:
    """
    shutdown the service

    Args:
        environment (str): environment name (e.g. Cloud9 IDE stack)
        service (str): name of the service

    Return: None
    """
    print(f"This is a shutdown of {service} from {environment}!")
```

Now let's get information about service feature:

```console
$ ./awesome service -h
usage: awesome service [-h] {new,shutdown,update} ...

positional arguments:
  {new,shutdown,update}
    new                 init the new project in given path
    shutdown            shutdown the service
    update              Updates the service...

optional arguments:
  -h, --help            show this help message and exit
```

How about each command?

```console
$ ./awesome service update -h
usage: awesome service update [-h] name version upgrade [args ...] [kwargs <name>=<value> ...]

positional arguments:
  name                  name of the service
  version               new version
  upgrade               if to upgrade everything
  args                  variable length arguments
  kwargs <name>=<value>
                        keyword arguments

optional arguments:
  -h, --help            show this help message and exit
```

Now let's call the update command:

```console
$ ./awesome service update myservice 2.0 True lib1 lib2 version1=1.2 version2=1.3

Updating... myservice to 2.0 with upgrade=True using ('lib1', 'lib2') and {'version1': 1.2, 'version2': 1.3}
```

As you have already noticed we have converted the CLI commands to the function arguments with proper type conversion.

## Versioning your features and commands

Now imagine the case, when for some reason you have a bunch of features with different versions and also your commands have different versioning.
You can easily handle it, by adding `__version__` in the feature and commands.

Open the `storage_X/cli/dev/service/__init__.py` and add:

```py hl_lines="3"
"""The service feature to handle our services"""

__version__ = "1.0"
```

Now you can get the version of the feature:

```console
$ ./awesome service --version

awesome service - v1.0
```

Same for `update` command:

```py title="update.py" hl_lines="1"
__version__ = "2.0"

def update(name: str, version: float, upgrade: bool, *args: str, **kwargs: float) -> None:
    ...
```

```console
$ ./awesome service update --version

awesome service update - v2.0
```

## Limiting the feature commands

You may have a situation, when you have other helper modules inside the feature package, and you do not want to expose them as a feature command.
In that case you can leverage the `__all__` mechanism. Originally in Python `__all__` only limits the imports such as: `from something import *`.
But here we use it just for eliminating the redundant operations when we register the feature commands.

So let's eliminate `shutdown` command from our `service` feature without removing it.

Update the `__init__.py` file of the service feature:

```py hl_lines="7"
"""The service feature to handle our services"""

from . import *

__version__ = "1.0"

__all__ = ["new", "update"]
```

And now try to get the help, as you have already noticed `shutdown` command is not available:

```console hl_lines="6"
$ ./awesome service -h

usage: awesome service [-h] [-v] {new,update} ...

positional arguments:
  {new,update}
    new          init the new project in given path
    update       Updates the service...

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

If you try to bypass this guard(because you know that there is a shutdown.py file indeed):

```console
$ ./awesome service shutdown -h

usage: awesome service [-h] [-v] {new,update} ...
awesome service: error: invalid choice: 'shutdown' (choose from 'new', 'update')
```

The next is to explore module as features.
