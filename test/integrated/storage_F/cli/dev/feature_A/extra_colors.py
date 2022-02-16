from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


def extra_colors(environment: str, *colors: Color) -> None:
    """
    Show me the colors: str, *args: Enum

    Args:
        environment (str): environment name (e.g. Cloud9 IDE stack)
        *colors (Enum): nice colors

    Return: None
    """
    print(f"{environment} -> {colors}")
