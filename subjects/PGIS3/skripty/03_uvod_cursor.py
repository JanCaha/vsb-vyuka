# ukázka použití SearchCursor
import arcpy
import arcpy.da
import utils

utils.setup_env("ProgrammingPro/Databases/Trippville_GIS.gdb")

feature_class = "Wetlands"

selected_attributes = [
    "OID@",
    "SHAPE@XY",
    "CLASS1",
    "NWI_CODE",
]

point = arcpy.Point(
    2_151_972.71,
    1_395_407.90,
)

i = 0
with arcpy.da.SearchCursor(
    feature_class,
    selected_attributes,
    spatial_reference=arcpy.SpatialReference(4326),
    where_clause="CLASS1 = 'EM'",
) as cursor:
    for row in cursor:
        print(f"ID: {row[0]} na souřadnicích {row[1]}")
        i = i + 1

print(f"Počet prvků: {i}")
