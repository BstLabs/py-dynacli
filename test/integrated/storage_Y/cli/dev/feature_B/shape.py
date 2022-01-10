from enum import Enum


class Shape(Enum):
    RECTANGLE = 1
    TRIANGLE = 2
    CIRCLE = 3


def shape(environment: str, shapes: Shape, *args: str, **kwargs: str) -> None:
    """
    Show me the shapes

    Args:
        environment (str): environment name (e.g. Cloud9 IDE stack)
        shapes (Enum): shape choices to accept

    Return: None
    """
    print(environment, shapes, args, kwargs)
