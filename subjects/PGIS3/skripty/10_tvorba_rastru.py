import arcpy
import utils

utils.setup_env("ProgrammingPro/Databases/Trippville_GIS.gdb")

raster = arcpy.Raster("DEM")

# načtení dat z rastru do NumPy pole
data = raster.read(upper_left_corner=(500, 500), ncols=1000, nrows=1000)

# raster info a úprava typu pixelu
raster_info: arcpy.RasterInfo = raster.getRasterInfo()
raster_info.setPixelType("U32")

# tvorba nového rastru dle objektu RasterInfo
raster_new = arcpy.Raster(raster_info)

# úprava dat vynásobením
data = data * 1000

# zápis dat do nového rastru
raster_new.write(data, upper_left_corner=(500, 500))

# zápis do nového rastru
raster_new.save("Raster_krat_1000")
print("Rastr x 1000 uložen.")

# tvorba nového rastru dle objektu RasterInfo z prázdného objektu
raster_info_2 = arcpy.RasterInfo()
raster_info_2.setSpatialReference(raster_info.getSpatialReference())
raster_info_2.setExtent(raster_info.getExtent())
raster_info_2.setCellSize((100, 100))
raster_info_2.setPixelType("U32")

raster_new_2 = arcpy.Raster(raster_info_2)

# načtení dat z prázdného rastru
data = raster_new_2.read()

# tvar dat - rozměry
print("=== Rozměry dat nového rastru ===")
print(data.shape)
print(data)
print("======")

# vypnění dat hodnotami
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        data[i, j, 0] = i * j

# zapis pole do rastru a uložení
raster_new_2.write(data)
raster_new_2.save("Raster_hodnoty_i_j")
print("Rastr hodnot i * j uložen.")
