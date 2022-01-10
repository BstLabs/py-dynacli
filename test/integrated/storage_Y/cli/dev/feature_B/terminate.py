from typing import Optional

__version__ = "3.3"


def terminate(
    environment: str, project: str, fraction: float, extra_fraction: Optional[float]
) -> None:
    """
    Terminator

    Args:
        project (str): name of the service
        environment (str): environment name (e.g. Cloud9 IDE stack)
        fraction (float): the fraction
        extra_fraction (float): extra fraction

    Return: None
    """
    print(environment, project, fraction, extra_fraction)
