def hello(*names: str) -> None:
    """
    Print Hello <first-name> <last-name> message

    Args:
        names (str): variable list of names to be included in greeting

    Return: None
    """
    print(f"Hello, {' '.join(names)}")
