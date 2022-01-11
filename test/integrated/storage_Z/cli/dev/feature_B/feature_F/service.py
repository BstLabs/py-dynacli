"""
This is an example of function as command
"""


def new(name: str) -> None:
    """
    Creates a new service - example of directly importing function

    Args:

        name (str): Name of project

    Return: None
    """
    print(f"This is a module as feature {name}")


def shutdown(name: str, environment: str) -> None:
    """
    Shutdown a service

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
