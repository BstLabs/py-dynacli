from enum import Enum
from typing import List


class Distance(Enum):
    LONG = 1
    SHORT = 2


def distance(highway: str, turns: List[int], *args: str, **kwargs: int) -> None:
    """
    Show me the distances

    Args:
        highway (str): The name of the highway
        turns (list): the list of the turns on the way
        **kwargs (str): the keyword length list of libraries
        *args (str): the variable length list of libraries

    Return: None
    """
    print(highway, turns, args, kwargs)
