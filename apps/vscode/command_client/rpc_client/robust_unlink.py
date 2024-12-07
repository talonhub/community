from pathlib import Path
from uuid import uuid4


def robust_unlink(path: Path):
    """Unlink the given file if it exists, and if we're on windows and it is
    currently in use, just rename it

    Args:
        path (Path): The path to unlink
    """
    try:
        path.unlink(missing_ok=True)
    except OSError as e:
        if hasattr(e, "winerror") and e.winerror == 32:
            graveyard_dir = path.parent / "graveyard"
            graveyard_dir.mkdir(parents=True, exist_ok=True)
            graveyard_path = graveyard_dir / str(uuid4())
            print(
                f"WARNING: File {path} was in use when we tried to delete it; "
                f"moving to graveyard at path {graveyard_path}"
            )
            path.rename(graveyard_path)
        else:
            raise e
