import math

import arcpy
import utils

utils.setup_env("ProgrammingPro/Databases/Trippville_GIS.gdb")

raster_1 = arcpy.Raster("DEM")
raster_2 = arcpy.Raster("Raster_hodnoty_i_j")
raster_3 = arcpy.Raster("Raster_krat_1000")
raster_3.readOnly = False

# raster cell iterátor se změnou některých dat
for i, j in raster_3:
    if raster_3[i, j] > 2_000_000:
        raster_3[i, j] = math.nan

# uložení změn
raster_3.save()
print(f"Raster {raster_3.catalogPath} upraven.")

# iterátor - řídí se prvním rastrem, jeho buňky jsou nastaveny jako řídící
with arcpy.sa.RasterCellIterator({"rasters": [raster_1, raster_2]}) as rci:
    count = 0
    for i, j in rci:
        count = count + 1
    print(f"Iterace dle rastru {raster_1.catalogPath} má {count} buněk.")

# vytvoření rastru dle šablony
raster_created = arcpy.Raster(raster_2.getRasterInfo())

# načtení celého rastru do NumPy pole
data = raster_created.read()

# výměna rastrů a průchod dle jiných buněk
with arcpy.sa.RasterCellIterator({"rasters": [raster_2, raster_1]}) as rci:
    count = 0
    for i, j in rci:
        values = rci[i, j]  # python tuple s hodnoty rastrů (zde 2)
        data[i, j] = values[0] / values[1]
        count = count + 1
    print(f"Iterace dle rastru {raster_2.catalogPath} má {count} buněk.")


raster_created.write(data)
raster_created.save("Raster_podil_rastru")

print("Nový raster vytvořen.")
