import typing

import arcpy


class RasterCellIteratorWrapper:
    """Wrapper pro arcpy.sa.RasterCellIterator s možností nastavení výchozích hodnot."""

    def __init__(
        self,
        rasters: typing.List[arcpy.Raster],
        padding=0,
        skip_no_data_rasters: typing.Optional[typing.List[arcpy.Raster]] = None,
    ):
        self.rasters = rasters
        self.padding = padding
        self.skip_no_data_rasters = skip_no_data_rasters if skip_no_data_rasters is not None else []
        self._iterator = None

    def __enter__(self):
        self._iterator = arcpy.sa.RasterCellIterator(
            {
                "rasters": self.rasters,
                "padding": self.padding,
                "skipNoData": self.skip_no_data_rasters,
            }
        )
        return self._iterator

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._iterator is not None:
            if hasattr(self._iterator, "__exit__"):
                self._iterator.__exit__(exc_type, exc_val, exc_tb)
            self._iterator = None
