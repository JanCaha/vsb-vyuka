from pathlib import Path


def data_path(filename: str) -> Path:
    file = Path(__file__).parent.parent / "_data" / filename
    return file
