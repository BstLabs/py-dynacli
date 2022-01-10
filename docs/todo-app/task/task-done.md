# todo task complete command

As described in original blog post: [Step 6](https://realpython.com/python-typer-cli/#step-6-code-the-to-do-completion-functionality)
we need to add complete command to mark the task as done by given ID.

First we need to update Todoer controller:

```py title="_todos/todo.py"

...

class Todoer:
    ...
    
    def set_done(self, todo_id: int) -> CurrentTodo:
        """Set a to-do as done."""
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list[self.project_name][todo_id - 1]
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        todo[0] = "Done"
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(write.todo_list, write.error)
    
    ...
```

The next thing is to create `complete.py` file in the `task` package:

```bash
$ tree
.
└── TODO
    ├── init.py
    ├── remove.py
    ├── rename.py
    ├── task
    │   ├── add.py
    │   ├── complete.py
    │   ├── delete.py
    │   ├── __init__.py
    │   └── list.py
    ├── todo
    └── _todos
        ├── database.py
        ├── __init__.py
        └── todo.py

3 directories, 12 files

```

Let's write our complete function:

```py title="task/complete.py"
from _todos import todo


def complete(project_name: str, task_id: int) -> None:
    """
    Set to done given task. Mark as complete.

    Args:
        project_name (str): the project name
        task_id (str): the task id to be removed
    
    Return: None
    """
    todo_ = todo.get_todoer(project_name)
    todo_.set_done(task_id)
    print("Success")

```

That's it, again no need for registering your command to CLI: it is already considered as CLI command.

Currently, we have 4 task commands:

```console
$ /todo task -h
usage: todo task [-h] {add,complete,delete,list} ...

positional arguments:
  {add,complete,delete,list}
    add                 Add task to the project
    complete            Set to done given task. Mark as complete.
    delete              Delete given task from the project
    list                Show all tasks in given project

optional arguments:
  -h, --help            show this help message and exit
```

Run the command:

```console
$ ./todo task list daily
ID. Is Done | Description
1 X morning walk
2 X night walk
3 X gym
4 X eat vegetables
```

```console
$ ./todo task complete daily 1
Success
```

```console hl_lines="3"
$ ./todo task list daily
ID. Is Done | Description
1 > morning walk
2 X night walk
3 X gym
4 X eat vegetables
```

As you have already noticed, the status has been changed from "X" to ">" marking it as a Done.

In raw, `daily.json` file it is updated as well:

`{"daily": [["Done", "morning walk"], ["Todo", "night walk"], ["Todo", "gym"], ["Todo", "eat vegetables"]]}`
