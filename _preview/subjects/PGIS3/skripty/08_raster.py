import arcpy
import utils

utils.setup_env("ProgrammingPro/Databases/Trippville_GIS.gdb")

raster = arcpy.Raster("DEM")

# základní info o rastru
print(f"{raster.width} - {raster.height}")
print(raster.pixelType)
print(raster.uncompressedSize)
print(raster.bandCount)
print(raster.bandNames)

# raster info o existujícím rastru
raster_info = raster.getRasterInfo()

# načtení dat z rastru do NumPy pole
# načítáme 100 x 100 pixelů od pozice 500, 500 z levého horního rohu
data = raster.read(upper_left_corner=(500, 500), nrows=100, ncols=100)

# základní info o načtených datech
print(data.shape)

# data
print(data)
