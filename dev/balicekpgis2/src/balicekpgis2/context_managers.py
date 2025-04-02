import pathlib
import types
import typing

from osgeo import gdal, ogr


class LayerContextManager:
    """Kontextový manager pro otevření OGR Vrstvy, gdal.Dataset se vytvoří automaticky"""

    def __init__(
        self,
        path: pathlib.Path,
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
