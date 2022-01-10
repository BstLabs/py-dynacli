# todo task delete command

We should be able to delete given task from given project.
Let's implement this command as well. You need to create `delete.py` file:

```bash
$ tree
.
└── TODO
    ├── init.py
    ├── remove.py
    ├── rename.py
    ├── task
    │   ├── add.py
    │   ├── delete.py
    │   ├── __init__.py
    │   └── list.py
    ├── todo
    └── _todos
        ├── database.py
        ├── __init__.py
        └── todo.py

3 directories, 11 files
```

Next, we need to add delete functionality to our Todoer controller.

The following code portion is from: [Implement the remove CLI Command](https://realpython.com/python-typer-cli/#implement-the-remove-cli-command)

```py title="_todos/todo.py"

...

class Todoer:
    ...
    
    def delete(self, task_id: int) -> CurrentTodo:
        """Delete a to-do from the database using its id or index."""
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            read.todo_list[self.project_name].pop(task_id - 1)
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(write.todo_list, write.error)
    
    ...

```

Add the actual delete command:

```py title="delete.py"
from _todos import todo


def delete(project_name: str, task_id: int) -> None:
    """
    Delete given task from the project

    Args:
        project_name (str): the project name
        task_id (str): the task id to be removed
    
    Return: None
    """
    todo_ = todo.get_todoer(project_name)
    todo_.delete(task_id)
    print("Success")
    
```

Let's test our delete command:

```console
$ ./todo task list daily
ID. Is Done | Description
1 X morning walk
2 X night walk
3 X gym
4 X eat vegetables
5 X eat fruits
```

Removing night walk from our daily routine(not in real life):

```console
$ ./todo task delete daily 5
Success
```

List tasks again:

```console
$ ./todo task list daily
ID. Is Done | Description
1 X morning walk
2 X night walk
3 X gym
4 X eat vegetables
```

Again, as you have already noticed everything is dead simple and CLI depends on what you wrote in pure Python, translating arguments to CLI arguments.
As a result, you don't have to write extra CLI command code - every function is already a command.
