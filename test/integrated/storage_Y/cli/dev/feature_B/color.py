from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


def color(environment: str, colors: Color) -> None:
    """
    Show me the colors

    Args:
        environment (str): environment name (e.g. Cloud9 IDE stack)
        colors (Enum): color choices to accept

    Return: None
    """
    print(f"{environment} -> {colors}")
