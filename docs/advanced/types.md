# Supported Python Types

Currently, we support following Python types as argument types in functions:

Supported: `int`, `float`, `str`, `bool`, `Enum`

Unsupported: `Optional[]`, `Union[]`, `list`, `tuple`, `dict` etc.

Even without unsupported type hints(and actual types) of arguments, you can easily replace them with `*args` and `**kwargs`, which are supported.
