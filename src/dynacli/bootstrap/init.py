import os
import shutil
import stat


def init(name: str, **kwargs: str) -> None:
    """
    Initialize the CLI entrypoint in given path

    Args:
        name (str): name of the new CLI tool
        **kwargs (str): The keyword arguments for CLI entrypoint

    Return: None
    """
    _wd = os.path.dirname(os.path.realpath(__file__))
    _path = kwargs.get("path")
    _cwd = _path if _path and _path != "." else os.path.curdir
    try:
        shutil.copyfile(f"{_wd}/_sample_cli", f"{_cwd}/{name}")
        os.chmod(f"{_cwd}/{name}", stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    except Exception as err:
        print("Failed to create CLI entrypoint with ", str(err))
    else:
        print(f"Successfully created CLI entrypoint {name} at {os.path.abspath(_cwd)}")
