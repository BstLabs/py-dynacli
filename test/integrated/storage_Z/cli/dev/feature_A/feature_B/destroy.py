def destroy(environment: str, project: str, *x: int, **y: int) -> None:
    """
    destroy the project and its libraries

    Args:
        project (str): name of the service
        environment (str): environment name (e.g. Cloud9 IDE stack)
        **y (str): the keyword length list of libraries
        *x (str): the variable length list of libraries

    Return: None
    """
    print(environment, project, x, y)
