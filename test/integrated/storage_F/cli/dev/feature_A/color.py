from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


def color(environment: str, *colors: Color, **kwargs: str) -> None:
    """
    Show me the colors: str, *args: Enum, **kwargs: str

    Args:
        environment (str): environment name (e.g. Cloud9 IDE stack)
        *colors (Enum): nice colors
        **kwargs (str): keyword arguments

    Return: None
    """
    print(f"{environment} -> {colors} -> {kwargs}")
