# todo remove command

Again, removing project(database) means removing our .json file.
The most naive way is to create `remove.py` file and pass the project name as argument:

```bash
$ tree
.
└── TODO
    ├── init.py
    ├── remove.py
    └── todo

1 directory, 3 files
```

```py title="remove.py"
import os

def remove(project_name: str) -> None:
    """
    Remove the .json file with given project name

    Args:
        project_name (str): The name of the project
    
    Return: None
    """
    os.remove(f"{project_name}.json")
    print("Removed: ", project_name)
```

Let's get help and remove our `daily` project:

```console
$ ./todo -h
usage: todo [-h] [-v] {init,remove} ...

TODO CLI APP

positional arguments:
  {init,remove}
    init         Initialize the .json file with given name
    remove       Remove the .json file with given project name

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

```console
$ ./todo remove daily
Removed:  daily
```

The final tree:

```console
$ tree -I __pycache__
.
├── init.py
├── remove.py
└── todo

0 directories, 3 files
```

The next command is `todo rename` which should rename our project.
