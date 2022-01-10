def shutdown(environment: str, service: str) -> None:
    """
    delete the service cloud formation stack

    Args:
        environment (str): environment name (e.g. Cloud9 IDE stack)
        service (str): name of the service

    Return: None
    """
    print(f"This is a shutdown of {service} from {environment}!")
