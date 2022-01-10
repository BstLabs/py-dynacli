# todo rename command

For renaming our project(database) we need old name and new name as function arguments to our `rename.py`.

```bash
$ tree
.
└── TODO
    ├── init.py
    ├── remove.py
    ├── rename.py
    └── todo

1 directory, 4 files
```

```py title="rename.py"
import os

def rename(old_name: str, new_name: str) -> None:
    """
    Rename the project name

    Args:
        old_name (str): old name of project
        new_name (str): new name of project
    
    Return: None
    """
    os.rename(f"{old_name}.json", f"{new_name}.json")
    print(f"Renamed: {old_name} {new_name}")
```

Get the help:

```console
$ ./todo rename -h
usage: todo rename [-h] old_name new_name

positional arguments:
  old_name    old name of project
  new_name    new name of project

optional arguments:
  -h, --help  show this help message and exit
```


Initializing:

```console
$ ./todo init daily
Created:  daily.json
```

```console
$ tree -I __pycache__
.
├── init.py
├── daily.json
├── remove.py
├── rename.py
└── todo

0 directories, 5 files
```

Renaming:

```console
$ ./todo rename daily DAILY
Renamed: daily DAILY
```

```console
$ tree -I __pycache__
.
├── init.py
├── DAILY.json
├── remove.py
├── rename.py
└── todo

0 directories, 5 files
```

So far our TODO CLI has 3 features:

```console
$ ./todo -h
usage: todo [-h] [-v] {init,remove,rename} ...

TODO CLI APP

positional arguments:
  {init,remove,rename}
    init                Initialize the .json file with given name
    remove              Remove the .json file with given project name
    rename              Rename the project name

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```

The next is to set up our task management commands.
