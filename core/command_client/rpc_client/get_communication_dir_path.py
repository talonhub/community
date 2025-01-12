import os
from pathlib import Path
from tempfile import gettempdir


def get_communication_dir_path(name: str) -> Path:
    """Returns directory that is used by command-server for communication

    Args:
        name (str): The name of the communication dir
    Returns:
        Path: The path to the communication dir
    """
    suffix = ""

    # NB: We don't suffix on Windows, because the temp dir is user-specific
    # anyways
    if hasattr(os, "getuid"):
        suffix = f"-{os.getuid()}"

    return Path(gettempdir()) / f"{name}{suffix}"
