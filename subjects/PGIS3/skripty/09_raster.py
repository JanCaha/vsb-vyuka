import arcpy
import utils

utils.setup_env("ProgrammingPro/Databases/Trippville_GIS.gdb")

raster = arcpy.Raster("DEM")

# základní info o rastru
print(f"Rozměry rastru: {raster.width} - {raster.height}")
print(f"Typy pixelu: {raster.pixelType}")
print(f"Velikost rastru v MB: {raster.uncompressedSize / (1024 * 1024)}")
print(f"Počet pásem: {raster.bandCount}")
print(f"Jména pásem: {raster.bandNames}")

# raster info o existujícím rastru
raster_info = raster.getRasterInfo()

# načtení dat z rastru do NumPy pole
# načítáme 100 x 100 pixelů od pozice 500, 500 z levého horního rohu
data = raster.read(upper_left_corner=(500, 500), nrows=100, ncols=100)
print(f"Typ data načtených pomocí funkce read: {type(data)}")

# základní info o načtených datech
print(f"Rozměry načtených dat: {data.shape}")

# data
print("=== Data načtená z rastru ===")
print(data)
