# Module as feature

Module as feature is a standalone module which is not located in the package(I.E it is not a package as feature).
It is a regular `.py` module file with functions in it - but it has no identical named function in it.

Let's add module as feature called `upload.py`:

```console
$ touch storage_X/cli/dev/upload.py
```

And add the docstring in the `upload.py` file:

``` py title="upload.py"
"""
This is an example of module feature
"""
```

If you run the CLI:

```bash
$ ./awesome -h
usage: awesome [-h] {service,upload,environment} ...

positional arguments:
  {service,upload,environment}
    service             The service feature to handle our services # (1)
    upload              This is an example of module feature # (2)
    environment         The environment feature to handle our environments # (3)

optional arguments:
  -h, --help            show this help message and exit
```

1. Package as feature from storage_X
2. Module as feature from storage_X
3. Package as feature from storage_Y

## Feature Commands

With package as feature the commands are modules with identical named functions in it.
In contrast, here we are going to add multiple functions in the `upload.py` - effectively multiple commands.

```py title="upload.py" hl_lines="32 41"
"""
This is an example of module feature
"""

def new(name: str) -> None:
    """
    uploads a new file

    Args:

        name (str): Name of file

    Return: None
    """
    print(f"This is a module as feature {name}")


def delete(name: str, environment: str) -> None:
    """
    Deletes a file from given environment

    Args:

        name (str): Name of project
        environment (str): Name of the env

    Return: None
    """
    print(f"Delete a module as feature {name} {environment}")


def _init():
    """
    This should not be shown
    
    Return: None
    """
    ...


def __revert():
    """
    This should not be shown

    Return: None
    """
    ...
```

**In Python convention something starting with single or double underscore considered as "protected" or "private".**

**We like this idea and those commands(functions) are silently ignored and are not considered as commands:**

```console hl_lines="5"
$ ./awesome upload -h 
usage: awesome upload [-h] {new,delete} ...

positional arguments:
  {new,delete}
    new         uploads a new file
    delete      Deletes a file from given environment

optional arguments:
  -h, --help    show this help message and exit
```

Finally, let's run this new command:

```console
$ ./awesome upload new -h
usage: awesome upload new [-h] name

positional arguments:
  name        Name of file

optional arguments:
  -h, --help  show this help message and exit
```

```console
$ ./awesome upload new file
This is a module as feature file
```

## Versioning module as feature

As with package as features you can add `__version__` in the module as feature to indicate your unique version:

``` py title="upload.py" hl_lines="5"
"""
This is an example of module feature
"""

__version__ = "5.0"

def new(name: str) -> None:
```

Now you can get the version as well:

```console
$ ./awesome upload new --version
awesome upload new - v5.0
```

## Limiting the feature commands

If for some reason you have a "public" function in the module, and you do not want to expose it as a command you can limit it by using `__all__`.

Originally in Python `__all__` only limits the imports such as: from something import *.

But here we use it just for eliminating the redundant operations when we register the feature commands:

```py title="upload.py" hl_lines="7"
"""
This is an example of module feature
"""

__version__ = "5.0"

__all__ = ["new"]

def new(name: str) -> None:
```

Now if you look at the help of the feature:

```console hl_lines="5"
$ ./awesome upload -h
usage: awesome upload [-h] [-v] {new} ...

positional arguments:
  {new}
    new          uploads a new file

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

And if you try to bypass(because you are sure there is a delete function):

```console hl_lines="3"
$ ./awesome upload delete -h
usage: awesome upload [-h] [-v] {new} ...
awesome upload: error: invalid choice: 'delete' (choose from 'new')
```

The next is to learn about top level commands.
