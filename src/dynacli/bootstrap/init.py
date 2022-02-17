import os
import shutil
import stat


def init(name: str, path: str) -> None:
    """
    Initialize the CLI entrypoint in given path

    Args:
        name (str): name of the new CLI tool
        path (str): The path for CLI entrypoint

    Return: None
    """
    wd = os.path.dirname(os.path.realpath(__file__))
    cwd = path if path != "." else os.path.curdir
    try:
        shutil.copyfile(f"{wd}/_sample_cli", f"{cwd}/{name}")
        os.chmod(f"{cwd}/{name}", stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    except Exception as err:
        print("Failed to create CLI entrypoint with ", str(err))
    else:
        print(f"Successfully created CLI entrypoint {name} at {cwd}")
