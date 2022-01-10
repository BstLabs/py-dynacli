# Top Level Command

Top level command is a module with identical named function in it. It is similar to package as a feature, except it is a module not package.
I.E it is a module as feature with identical named function in it.

Let's create sample one:

```console
$ touch storage_X/cli/dev/destroy.py
```

Define the command as:

```py title="destroy.py"
def destroy(name: str) -> None:
    """
    Destroy given name...(top level command)

    Args:

        name (str): Name of project

    Return: None
    """
    print(f"This is a top level destroyer - {name}")
```

Get the help message:

```bash
$ ./awesome -h
usage: awesome [-h] {destroy,service,upload,environment} ...

positional arguments:
  {destroy,service,upload,environment}
    destroy             Destroy given name...(top level command) # (1)
    service             The service feature to handle our services # (2)
    upload              This is an example of module feature # (3)
    environment         The environment feature to handle our environments # (4)

optional arguments:
  -h, --help            show this help message and exit
```

1. Top level command from storage_X
2. Package as feature from storage_X
3. Module as feature from storage_X
4. Package as feature from storage_Y

Get the top level command help:

```console
$ ./awesome destroy -h
usage: awesome destroy [-h] name

positional arguments:
  name        Name of project

optional arguments:
  -h, --help  show this help message and exit
```

Run the top level command:

```console
$ ./awesome destroy please
This is a top level destroyer - please
```

## Versioning

You can add a unique version to your top level command by adding `__version__`:

```py title="destroy.py" hl_lines="1"
__version__ = "1.1a1"

def destroy(name: str) -> None:
```

Get the version information:

```console hl_lines="9"
./awesome destroy -h
usage: awesome destroy [-h] [-v] name

positional arguments:
  name           Name of project

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

```console
$ ./awesome destroy --version
awesome destroy - v1.1a1
```
