from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


def colors(environment: str, *colors: Color, **new_colors: Color) -> None:
    """
    Show me the colors: str, *args: Enum, **kwargs: Enum

    Args:
        environment (str): environment name (e.g. Cloud9 IDE stack)
        *colors (Enum): nice colors
        **new_colors (Enum): color choices to accept

    Return: None
    """
    print(f"{environment} -> {colors} -> {new_colors}")
