import types
import typing
import warnings
from pathlib import Path

from osgeo import gdal, ogr


def base_data_path() -> Path:
    """Vrací cestu ke složce s daty jako objekt Path."""
    return Path(__file__).parent.parent / "_data"


def data_path(filename: str) -> Path:
    """Vrací cestu k souboru s daným názvem souboru jako objekt Path. Pokud soubor neexistuje vyvolá chybu."""
    file = base_data_path() / filename
    if not file.exists():
        raise ValueError(f"File {file.as_posix()} does not exist.")
    return file


def base_save_data_path() -> Path:
    """Vrací cestu ke složce pro uložení dat jako objekt Path. Pokud složka neexistuje, vytvoří ji."""
    path = base_data_path() / "saved"
    if not path.exists():
        path.mkdir(parents=True)
    return path


def save_data_path(filename: str, delete_if_exist: bool = False) -> Path:
    """Vrací cestu k souboru pro uložení dat jako objekt Path. Pokud soubor existuje, vyvolá varování a pokud je nastaveno delete_if_exist na True, soubor smaže."""
    path = base_save_data_path() / filename
    if path.exists():
        warnings.warn(f"File {path.as_posix()} exists.")
        if delete_if_exist:
            warnings.warn("File was deleted!")
            path.unlink()
    return path


class LayerContextManager:
    """Kontextový manager pro otevření OGR Vrstvy, gdal.Dataset se vytvoří automaticky"""

    def __init__(
        self,
        path: Path,
        layer: typing.Optional[typing.Union[int, str]] = None,
    ):
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

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ):
        self.layer = None
        self.ds = None


class LayerFromDatasetContextManager:
    """Kontextový manager pro otevření OGR Vrstvy z gdal.Datasetu"""

    def __init__(
        self,
        ds: gdal.Dataset,
        layer: typing.Optional[typing.Union[int, str]] = None,
    ):
        self.selected_layer = layer
        self.ds: gdal.Dataset = ds
        self.layer: ogr.Layer = None

    def __enter__(self) -> ogr.Layer:
        if isinstance(self.selected_layer, int):
            self.layer = self.ds.GetLayer(self.selected_layer)
        elif isinstance(self.selected_layer, str):
            self.layer = self.ds.GetLayerByName(self.selected_layer)
        else:
            self.layer = self.ds.GetLayer()
        if self.layer is None:
            raise ValueError("Layer not found.")

        return self.layer

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ):
        self.layer = None


class BandAsArrayContextManager:
    """Kontextový manager pro otevření rastru a vrácení pásma rastru"""

    def __init__(self, ds: gdal.Dataset, band_number: int = 1):
        self.band_number = band_number
        self.ds: gdal.Dataset = ds
        self.band: gdal.Band = None

    def __enter__(self) -> gdal.Band:

        self.band = self.ds.GetRasterBand(self.band_number)

        if self.band is None:
            raise ValueError("Band not found.")

        return self.band

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ):
        self.band = None
