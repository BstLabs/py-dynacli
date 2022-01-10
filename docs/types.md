# Python types

If you need a refresher about how to use Python type hints, read here [Python Type Checking (Guide)](https://realpython.com/python-type-checking/).

You can also check the [mypy cheat sheet](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html).
In short (very short), you can declare a function with parameters like:

```Python
from enum import Enum

class Color(Enum):
    WHITE = 1
    RED = 2

def type_example(name: str, formal: bool, exit: int, amount: float, color: Color, *args: str, **kwargs: int):
    pass
```

And your editor (and **DynaCLI**) will know that:

* `name` is type of `str` and is a required parameter.
* `formal` is type of `bool` and is a required parameter.
* `exit` is type of `int` and is a required parameter.
* `amount` is type of `float` and is a required parameter.
* `color` is type of `Color` and is a required parameter.
* `*args` variable length arguments with type of `str`.
* `**kwargs` keyword arguments with type of `int`.

These type hints are what give you autocomplete in your editor and several other features.

**DynaCLI** is based on these type hints.
