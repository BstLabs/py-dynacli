def create(environment: str, project: str, **kwargs: str) -> None:
    """
    create the project and its libraries

    Args:
        environment (str): environment name (e.g. Cloud9 IDE stack)
        project (str): name of the service
        **kwargs (str): the keyword length list of libraries

    Return: None
    """
    print(environment, project, kwargs)
