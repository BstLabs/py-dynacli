# todo init command

The simplest way of storing our todos is constructing a .json file with given name.
At this point it is different from [original post](https://realpython.com/python-typer-cli/), 
and we consider it is simpler to store tasks as: `(Status, Task name)` style in `.json` file.
We consider the database as a project name where the tasks should reside.
If you want to create a task management for your daily routine - that means, we need to init the daily database(or daily project).

This is called initialization, so we have created `init.py` file:

```bash
$ tree
.
└── TODO
    ├── init.py
    └── todo

1 directory, 2 files
```

```py title="init.py"
import json

def init(project_name: str) -> None:
    """
    Initialize the .json file with given name

    Args:
        project_name (str): the name of the todo project
    
    Return: None
    """
    data = {project_name: []}
    with open(f"{project_name}.json", "w") as f:
        json.dump(data, f)
    print("Created: ", project_name+".json")
```

That is it now we have nice help message, and we can initialize our "database" json file:

```console
$ ./todo init -h
usage: todo init [-h] project_name

positional arguments:
  project_name  the name of the todo project

optional arguments:
  -h, --help    show this help message and exit
```

Run the init command:

```console
$ ./todo init daily
Created:  daily.json
```

The final tree:

```console
$ tree -I __pycache__
.
├── init.py
├── daily.json
└── todo

0 directories, 3 files
```

The next command is to implement `todo remove` command - I.E deleting .json file.
