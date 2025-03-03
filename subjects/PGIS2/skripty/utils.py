import typing
import warnings
from pathlib import Path

from osgeo import gdal, ogr


def base_data_path() -> Path:
    """Returns a path to the data directory as a Path object."""
    return Path(__file__).parent.parent / "_data"


def data_path(filename: str) -> Path:
    """Returns a path to a file as a Path object or raises an error if file does not exist."""
    file = base_data_path() / filename
    if not file.exists():
        raise ValueError(f"File {file.as_posix()} does not exist.")
    return file


def save_data_path(filename: str, delete_if_exist: bool = False) -> Path:
    """Returns a path to a file as a Path object. If the file exists, it prints a warning. Optionally, the file can be deleted."""
    path = base_data_path() / "saved" / filename
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    if path.exists():
        warnings.warn(f"File {path.as_posix()} exists.")
        if delete_if_exist:
            warnings.warn("File was deleted!")
            path.unlink()
    return path


class LayerContextManager:
    """Kontextový manager pro otevření OGR Vrstvy"""

    def __init__(self, path: Path, layer: typing.Optional[typing.Union[int, str]] = None):
        self.path = path
        self.selected_layer = layer
        self.ds: gdal.Dataset = None
        self.layer: ogr.Layer = None

    def __enter__(self) -> ogr.Layer:
        self.ds = gdal.OpenEx(self.path.as_posix())
        if self.ds is None:
            raise ValueError(f"File `{self.path.as_posix()}` not found or cannot be opened.")
        if isinstance(self.selected_layer, int):
            self.layer = self.ds.GetLayer(self.selected_layer)
        elif isinstance(self.selected_layer, str):
            self.layer = self.ds.GetLayerByName(self.selected_layer)
        else:
            self.layer = self.ds.GetLayer()
        if self.layer is None:
            raise ValueError("Layer not found.")
        return self.layer

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.layer = None
        self.ds = None
