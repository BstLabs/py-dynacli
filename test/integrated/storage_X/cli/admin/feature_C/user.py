def user(first_name: str, last_name: str, **kwargs: str) -> None:
    """
    get the name and last name and other information of the user

    Args:
        first_name (str): name of the user
        last_name (str): last name of the user
        *kwargs (str): keyword arguments

    Return: None
    """
    print(first_name, last_name, kwargs)
