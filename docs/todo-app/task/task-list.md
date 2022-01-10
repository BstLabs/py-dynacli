# todo task list command

It should be easier to get back registered tasks back using CLI, rather than looking at `.json` files.
So we are going to add simple command to list available tasks in the given project.
We have changed the implementation described here: [Implement the list Command](https://realpython.com/python-typer-cli/#implement-the-list-command) 

Create `list.py` file:

```bash
$ tree
.
└── TODO
    ├── init.py
    ├── remove.py
    ├── rename.py
    ├── task
    │   ├── add.py
    │   ├── __init__.py
    │   └── list.py
    ├── todo
    └── _todos
        ├── database.py
        ├── __init__.py
        └── todo.py

3 directories, 10 files
```

Implementation:

```py title="list.py"
import os
from _todos import todo


def list(project_name: str) -> None:
    """
    Show all tasks in given project

    Args:
        project_name (str): the project name
    
    Return: None
    """
    todo_ = todo.get_todoer(project_name)
    todo_list = todo_.get_todo_list()
    _format_output(todo_list)


def _format_output(stdout: list[list[str, any]]) -> None:
    headers = ("ID. ", "Is Done ", "| Description")
    print("".join(headers))
    for id_, t in enumerate(stdout, 1):
        status = "X" if t[0] == 'Todo' else ">"
        print(id_, status, t[1])
```

Now, we need to add `get_todo_list()` method to the Todoer class:

```py title="_todos/todo.py" hl_lines="7"

...

class Todoer:
    
    ...
    
    def get_todo_list(self) -> list[list[str, Any]]:
        """Return the current to-do list."""
        read = self._db_handler.read_todos()
        return read.todo_list[self.project_name]


...

```

Getting help and running the command:

```console
$ ./todo task list -h
usage: todo task list [-h] project_name

positional arguments:
  project_name  the project name

optional arguments:
  -h, --help    show this help message and exit
```

**If you have noticed, the `_format_output()` function was not considered as a command - as it is a "non-public" function based on Python convention.**

Let's run the actual command:

```console
$ ./todo task list daily
ID. Is Done | Description
1 X morning walk
2 X night walk
3 X gym
4 X eat vegetables
5 X eat fruits
```

How about to add separate versions to our commands? It is possible to have different commands from various resources, and they can have different versioning.
It is easy to implement it with DynaCLI, just add `__version__` to the `list.py` file:

```py title="list.py" hl_lines="6"
import os
from _todos import todo

__version__ = "1.1"
```

Checking versions:

```console
$ ./todo --version
todo - v1.0
```

```console
$ ./todo task list --version
todo task list - v1.1
```

So your main CLI and your commands can have different versions.

The next is to add a command for deleting the task.
