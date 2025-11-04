import math

import arcpy
import utils

utils.setup_env("ProgrammingPro/Databases/Trippville_GIS.gdb")

raster_1 = arcpy.Raster("DEM")
raster_2 = arcpy.Raster("New_Raster_2")
raster_3 = arcpy.Raster("New_Raster")
raster_3.readOnly = False

# raster cell iterátor se změnou některých dat
for i, j in raster_3:
    if raster_3[i, j] > 2_000_000:
        raster_3[i, j] = math.nan

# uložení změn
raster_3.save("New_Raster")

# iterátor - řídí se prvním rastrem, jeho buňky jsou nastaveny jako řídící
with arcpy.sa.RasterCellIterator({"rasters": [raster_1, raster_2]}) as rci:
    count = 0
    for i, j in rci:
        count = count + 1
    print(count)

# výměna rastrů a průchod dle jiných buněk
with arcpy.sa.RasterCellIterator({"rasters": [raster_2, raster_1]}) as rci:
    count = 0
    for i, j in rci:
        count = count + 1
    print(count)
