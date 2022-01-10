def package(environment: str, project: str, *args: str) -> None:
    """
    package the project and its libraries

    Args:
        environment (str): environment name (e.g. Cloud9 IDE stack)
        project (str): name of the service
        *args (str): the variable length list of libraries

    Return: None
    """
    print(environment, project, args)
