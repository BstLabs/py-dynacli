__version__ = "1.2"


def destroy(environment: str, project: str, *args: str, **kwargs: str) -> None:
    """
    destroy the project and its libraries

    Args:
        project (str): name of the service
        environment (str): environment name (e.g. Cloud9 IDE stack)
        **kwargs (str): the keyword length list of libraries
        *args (str): the variable length list of libraries

    Return: None
    """
    print(environment, project, args, kwargs)
