# todo task add command

As task management logically is a group of commands it is better to add them in `task` package:

```bash
$ tree
.
└── TODO
    ├── init.py
    ├── remove.py
    ├── rename.py
    ├── task
    │   └── __init__.py
    ├── todo
    └── _todos
        ├── database.py
        ├── __init__.py
        └── todo.py

3 directories, 8 files
```

```py title="__init__.py"
"""
Task management commands
"""
```

Get the overall help:

```console
$ ./todo -h
usage: todo [-h] [-v] {init,remove,rename,task} ...

TODO CLI APP

positional arguments:
  {init,remove,rename,task}
    init                Initialize the .json file with given name
    remove              Remove the .json file with given project name
    rename              Rename the project name
    task                Task management commands

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```

**As you may notice the `_todos` package was ignored as it is considered as "non-public" - pure Python convention.**

So, the DynaCLI does not interfere any already existing code base.

To implement the task adding, we need to create `add.py` file:

```bash
tree
.
└── TODO
    ├── init.py
    ├── remove.py
    ├── rename.py
    ├── task
    │   ├── add.py
    │   └── __init__.py
    ├── todo
    └── _todos
        ├── database.py
        ├── __init__.py
        └── todo.py

3 directories, 9 files
```

Here we use as a reference [Implement the add CLI Command](https://realpython.com/python-typer-cli/#implement-the-add-cli-command).

And of course define the add function in the `add.py`:

```py title="add.py"
from _todos import todo


def add(project_name: str, task: str, *tasks: str) -> None:
    """
    Add task to the project

    Args:
        project_name (str): the project name
        task (str): task name
        *tasks (str): variable length argument
    
    Return: None
    """
    todo_ = todo.get_todoer(project_name)
    for t in [task, *tasks]:
        todo_.add(t)

    print("Success")
```

Next is to add the implementations of `add` and `add_multiple` methods in Todoer class:

```py title="_todos/todo.py" hl_lines="20 28"
import os
from .database import DatabaseHandler
from typing import NamedTuple, Any
from . import DB_READ_ERROR


DIR = os.path.dirname(__file__)


class CurrentTodo(NamedTuple):
    todo: dict[str, list[tuple[str]]]
    error: int


class Todoer:
    def __init__(self, project_name: str) -> None:
        self.project_name = project_name
        self._db_handler = DatabaseHandler(DIR + f"/../{project_name}.json")

    def add(self, task: str) -> CurrentTodo:
        read = self._db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return CurrentTodo(read.todo_list, read.error)
        read.todo_list[self.project_name].append(["Todo", task])
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(write.todo_list, write.error)

    def add_multiple(self, tasks: tuple[str]) -> None:
        read = self._db_handler.read_todos()
        for task_ in tasks:
            read.todo_list[self.project_name].append(["Todo", task_])
            self._db_handler.write_todos(read.todo_list)


def get_todoer(project_name: str) -> Todoer:
    return Todoer(project_name)
```

Now let's test our CLI:

```console
$ ./todo init daily
Created:  daily.json
```

Adding 2 daily tasks:

```console

$ ./todo task add daily "morning walk"
Success

$ ./todo task add daily "night walk"
Success
```

Now the daily.json file looks like: `{"daily": [["Todo", "morning walk"], ["Todo", "night walk"]]}`.

How about adding multiple tasks in one shot?

Adding multiple daily tasks:

```console
$ ./todo task add daily gym "eat vegetables" "eat fruits"
Success
```

If you check the `daily.json`: `{"daily": [["Todo", "morning walk"], ["Todo", "night walk"], ["Todo", "gym"], ["Todo", "eat vegetables"], ["Todo", "eat fruits"]]}`

If you have already noticed every task is by default marked as `"Todo"`.

The next topic is to add `todo task list` command.
