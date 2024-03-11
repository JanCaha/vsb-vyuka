# NOTE: kontorla typu souboru pomocí driveru, otevření rastru a zjištění
# detailů o rastru a pásmu
from pathlib import Path

from osgeo import gdal

gdal.UseExceptions()

if __name__ == "__main__":
    file = Path(__file__).parent.parent.parent / "_data" / "HYP_HR_SR_OB_DR.tif"

    print(file.exists())

    driver: gdal.Driver = gdal.IdentifyDriverEx(file.as_posix())

    print(f"Driver: {driver.LongName}")

    ds: gdal.Dataset = gdal.OpenEx(file.as_posix())

    print(f"Number of bands: {ds.RasterCount}")

    band: gdal.Band = ds.GetRasterBand(1)

    print(f"Band Size: {band.XSize} - {band.YSize}")
    print(f"Band data type: {gdal.GetDataTypeName(band.DataType)}")
