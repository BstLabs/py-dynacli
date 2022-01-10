def change(name: str) -> None:
    # Command with mismatched argument name in docstring and function definition
    """
    change the name

    Args:
        kkk (str): wrong argument name


    Return: None
    """
    print(f"Change {name=}")


def remove(name: str) -> None:
    # Command with missing  in docstring
    """
    remove the name

    Args:

    Return: None
    """
    print(f"Remove {name=}")


def drop(name: str) -> None:
    # Command with missing return in docstring
    """
    drop the name

    Args:
        name (str): We love to drop
    """
    print(f"Drop {name=}")


def detect(name: str) -> None:
    # Command with only description docstring
    """
    detect the name
    """
    print(f"Detect {name=}")


def lonely() -> None:
    # Command with no docstring
    print("I am alone here")


def love(name: str) -> None:
    # Command with no docstring
    print(f"Love {name=}")


def unsupported(name: str) -> None:
    # Command with docstring with wrong type in it
    """
    unsupported name

    Args:
        name str: should fail

    Return: None
    """
    print(name)
