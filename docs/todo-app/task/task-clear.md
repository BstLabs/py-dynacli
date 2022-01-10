# todo task clear command

How about removing all tasks? I.E clearing the project?

The idea is similar to the [Implement the clear CLI Command](https://realpython.com/python-typer-cli/#implement-the-clear-cli-command)

First, we need to update Todoer controller:

```py title="_todos/todo.py"
...

class Todoer:
    
    ...
    
    def remove_all(self) -> CurrentTodo:
        """Remove all to-dos from the database."""
        write = self._db_handler.write_todos({f"{self.project_name}": []})
        return CurrentTodo({}, write.error)
        
    ...
```

The next thing is to create `clear.py` file in the `task` package:

```bash
$ tree
.
└── TODO
    ├── init.py
    ├── remove.py
    ├── rename.py
    ├── task
    │   ├── add.py
    │   ├── clear.py
    │   ├── complete.py
    │   ├── delete.py
    │   ├── __init__.py
    │   └── list.py
    ├── todo
    └── _todos
        ├── database.py
        ├── __init__.py
        └── todo.py

3 directories, 13 files
```


The actual implementation is similar to the original blog post, here we are intentionally using decorator as a prompt:

```py title="task/clear.py"
from functools import wraps
from _todos import todo


def _prompt(func_: callable) -> callable:
    @wraps(func_)
    def wrapper(project_name: str):
        while True:
            choice = input("Delete all to-dos? [y/N]:")
            if 'y' == choice:
                return func_(project_name)
            elif 'N' == choice:
                print('Operation cancelled')
                exit(1)
            print('Invalid choice. Try again')

    return wrapper


@_prompt
def clear(project_name: str) -> None:
    """
    Deleting all tasks
    
    Args:
        project_name (str): the project name

    Return: None
    """
    todo_ = todo.get_todoer(project_name)
    todo_.remove_all()

    print("All to-dos were removed")

```

Get the help of the clear command:

```console
$ ./todo task clear -h
usage: todo task clear [-h] project_name

positional arguments:
  project_name  the project name

optional arguments:
  -h, --help    show this help message and exit
```

**As you see, the actual code and also the `DynaCLI` implementation did not interfere with `_prompt` decorator.**

Let's test our clear command:

```console
$ ./todo task list daily
ID. Is Done | Description
1 > morning walk
2 X night walk
3 X gym
4 X eat vegetables
```

```console
$ ./todo task clear daily
Delete all to-dos? [y/N]:N
Operation canceled
```

```console
./todo task clear daily
Delete all to-dos? [y/N]:sasd
Invalid choice. Try again
Delete all to-dos? [y/N]:y
All to-dos were removed
```

```console
$ /todo task list daily
ID. Is Done | Description
```

Dead simple. `DynaCLI` just converted `clear` function to the CLI `clear` command(yes it works with **decorated** functions).
