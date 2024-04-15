import warnings
from pathlib import Path


def data_path(filename: str) -> Path:
    """Returns a path to a file as a Path object or raises an error if file does not exist."""
    file = Path(__file__).parent.parent / "_data" / filename
    if not file.exists():
        raise ValueError(f"File {file.as_posix()} does not exist.")
    return file


def get_save_data_path(filename: str, delete_if_exist: bool = False) -> Path:
    """Returns a path to a file as a Path object. If the file exists, it prints a warning. Optionally, the file can be deleted."""
    path = Path(__file__).parent.parent / "_data" / "saved" / filename
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    if path.exists():
        warnings.warn(f"File {path.as_posix()} exists.")
        if delete_if_exist:
            warnings.warn("File was deleted!")
            path.unlink()
    return path
