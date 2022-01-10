# Setup todo controller class

This section is primarily adopted from [Step 4](https://realpython.com/python-typer-cli/#step-4-set-up-the-to-do-app-back-end) and [Step 5](https://realpython.com/python-typer-cli/#step-5-code-the-adding-and-listing-to-dos-functionalities)

Again we have omitted redundant parts and keep only needed code portions.

Let's create `todo.py` file in our `_todos` package:

```bash
$ tree
.
└── TODO
    ├── init.py
    ├── remove.py
    ├── rename.py
    ├── todo
    └── _todos
        ├── database.py
        ├── __init__.py
        └── todo.py

2 directories, 7 files
```

And add our controller class:

```py title="todo.py"
import os
from .database import DatabaseHandler
from typing import NamedTuple, Any
from . import DB_READ_ERROR, ID_ERROR

DIR = os.path.dirname(__file__)


class CurrentTodo(NamedTuple):
    todo: dict[str, list[list[str, Any]]]
    error: int


class Todoer:
    def __init__(self, project_name: str) -> None:
        self.project_name = project_name
        self._db_handler = DatabaseHandler(DIR + f"/../{project_name}.json")


def get_todoer(project_name: str) -> Todoer:
    return Todoer(project_name)
```

We have added `get_todoer` function to get back the Todoer object - it will be used in the actual CLI commands.

The next is to implement the task adding CLI command.
