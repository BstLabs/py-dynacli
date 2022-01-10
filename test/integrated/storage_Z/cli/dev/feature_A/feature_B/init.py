from typing import Optional


def init(name: str, path: Optional[str] = None):
    """
    init the project in given path

    Args:
        name (str): name of the project
        path (str): name of the path

    Return: None
    """
    print(f"Initializing the {name} in {path}")
