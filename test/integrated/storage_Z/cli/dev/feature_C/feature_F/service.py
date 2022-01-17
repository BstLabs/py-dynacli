"""
This is an example of module - which is imported in __init__.py
"""


def new(name: str) -> None:
    """
    Creates a new service - example of directly importing module in __init__.py

    Args:

        name (str): Name of project (function as command)

    Return: None
    """
    print(f"This is a callable as a command {name}")


def shutdown(name: str, environment: str) -> None:
    """
    Shutdown a service - example of directly importing module in __init__.py

    Args:

        name (str): Name of project
        environment (str): Name of the env

    Return: None
    """
    print(f"Shutdown a module as feature {name} {environment}")


def _init():
    """
    This should not be shown
    :return:
    """
    ...


def __revert():
    """
    This should not be shown
    :return:
    """
    ...
