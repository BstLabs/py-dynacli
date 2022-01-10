# Setup the database operations

Here we grab [Step 2](https://realpython.com/python-typer-cli/#step-2-set-up-the-to-do-cli-app-with-python-and-typer) and [Step 4](https://realpython.com/python-typer-cli/#step-4-set-up-the-to-do-app-back-end
) from the original article and mostly ignored other code portions.

As we have several helper code we can store them in the `_todos` package:

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
        └── __init__.py

2 directories, 6 files

```

Let's add some preliminary constants:


```py title="__init__.py"
(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    ID_ERROR: "to-do id error",
}
```

As you may notice we have removed redundant app name and version information from the `__init__.py` which was described in [Step 2](https://realpython.com/python-typer-cli/#step-2-set-up-the-to-do-cli-app-with-python-and-typer).

Let's add our database handler class:

```py title="database.py"
import json
from typing import NamedTuple, Any
from . import JSON_ERROR, SUCCESS, DB_READ_ERROR, DB_WRITE_ERROR


class DBResponse(NamedTuple):
    todo_list: dict[str, list[list[str, Any]]]
    error: int


class DatabaseHandler:

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def read_todos(self) -> DBResponse:
        try:
            with open(self._db_path, "r") as db:
                try:
                    return DBResponse(json.loads(db.readline()), SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse({}, JSON_ERROR)
        except OSError:  # Catch file IO problems
            return DBResponse({}, DB_READ_ERROR)

    def write_todos(self, todo_list: dict[str, list[list[str, Any]]]) -> DBResponse:
        try:
            with open(self._db_path, "w") as db:
                json.dump(todo_list, db)
            return DBResponse(todo_list, SUCCESS)
        except OSError:  # Catch file IO problems
            return DBResponse(todo_list, DB_WRITE_ERROR)
```

Again, we have slightly changed the code but most of it is from [Step 4](https://realpython.com/python-typer-cli/#step-4-set-up-the-to-do-app-back-end).

We added extra package to our CLI path, it should be broken right now? Of course not.

In pure Python convention the names which are started with `_`(underscore) are considered as "non-public".
DynaCLI follows this convention, and we just **ignore "non-public" packages** - they are not considered as part of CLI.

The next is to add a Controller class for our TODOs.
