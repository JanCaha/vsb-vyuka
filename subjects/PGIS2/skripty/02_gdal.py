# NOTE: kontrola typu souboru pomocí driveru, otevření rastru a zjištění
# detailů o rastru a pásmu

from osgeo import gdal
from utils import data_path

gdal.UseExceptions()

if __name__ == "__main__":
    file = data_path("HYP_HR_SR_W.tif")

    print(file.exists())

    driver: gdal.Driver = gdal.IdentifyDriverEx(file)

    print(f"Driver: {driver.LongName}")

    ds: gdal.Dataset = gdal.OpenEx(file)

    print(f"Number of bands: {ds.RasterCount}")

    band: gdal.Band = ds.GetRasterBand(1)

    print(f"Band Size: {band.XSize} - {band.YSize}")
    print(f"Band data type: {gdal.GetDataTypeName(band.DataType)}")

    data = band.ReadAsArray(0, 0, band.XSize, band.YSize)

    # je vhodné explicitně uvolnit paměť těchto proměnných
    band = None
    ds = None
