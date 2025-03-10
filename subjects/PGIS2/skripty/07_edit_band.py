import numpy as np
import utils
from osgeo import gdal

gdal.UseExceptions()

if __name__ == "__main__":
    file = utils.data_path("HYP_HR_SR_W.tif")
    file_export = utils.save_data_path("edited.tif")

    ds: gdal.Dataset = gdal.Translate("/vsimem/edited.tif", file)

    with utils.BandAsArrayContextManager(ds, 2) as band:
        offset = 1000
        data: np.ndarray = band.ReadAsArray(offset, offset, 5000, 2000)

        data_edited = np.zeros_like(data)

        band.WriteArray(data_edited, offset, offset)

    gdal.Translate(file_export, ds)

    ds = None
