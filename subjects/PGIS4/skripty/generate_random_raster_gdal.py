import numpy as np
import utils
from osgeo import gdal, osr

gdal.UseExceptions()

# Rozsah ČR v S-JTSK (EPSG:5514)
# xmin, ymin, xmax, ymax (přibližně)
extent = (-930000, -1230000, -400000, -920000)
cell_size = 100  # velikost buňky v metrech

# Výpočet počtu sloupců a řádků
cols = int((extent[2] - extent[0]) / cell_size)
rows = int((extent[3] - extent[1]) / cell_size)

# Vytvoření náhodného pole
random_data = np.random.rand(rows, cols) * 1000

# Vytvoření rasteru pomocí GDAL
output_file = utils.save_data_path("nahodny_raster.tif").as_posix()
driver: gdal.Driver = gdal.GetDriverByName("GTiff")
dataset: gdal.Dataset = driver.Create(output_file, cols, rows, 1, gdal.GDT_Float32)

dataset.SetGeoTransform(
    [
        extent[0],
        cell_size,
        0,  # x origin, pixel width, rotation
        extent[3],
        0,
        -cell_size,  # y origin, rotation, pixel height (negativní)
    ]
)

# Nastavení SRS na EPSG:5514
srs = osr.SpatialReference()
srs.ImportFromEPSG(5514)
dataset.SetProjection(srs.ExportToWkt())

dataset.GetRasterBand(1).WriteArray(random_data)
dataset.GetRasterBand(1).SetNoDataValue(0)

dataset.FlushCache()
dataset = None

print(f"Random raster created: {output_file}")
