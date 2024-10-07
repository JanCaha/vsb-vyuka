# ukázka použití kurzorů
import arcpy
import arcpy.da
import arcpy.management
import utils

utils.setup_env("ProgrammingPro/Databases/Trippville_GIS.gdb")

feature_class = "Wetlands"

selected_attributes = [
    "OID@",
    "SHAPE@",
    "CLASS1",
    "NWI_CODE",
]

layer_to_edit = "NewLayer"

# kopírování vrstvy
arcpy.management.Copy(feature_class, layer_to_edit)

# úprava kopie vrstvy pro vybrané prvky
with arcpy.da.UpdateCursor(
    layer_to_edit,
    selected_attributes,
    where_clause="CLASS1 = 'EM'",
) as cursor:
    for row in cursor:
        geom: arcpy.Geometry = row[1]
        extent: arcpy.Extent = geom.extent
        row[1] = extent.polygon
        row[2] = "AA"
        cursor.updateRow(row)

# mazání prvků
with arcpy.da.UpdateCursor(
    layer_to_edit,
    selected_attributes,
    where_clause="CLASS1 = 'SS'",
) as cursor:
    for row in cursor:
        cursor.deleteRow()

# vlození nového prvku
with arcpy.da.InsertCursor(
    layer_to_edit,
    ["SHAPE@", "CLASS1"],
) as cursor:
    geom = arcpy.PointGeometry(arcpy.Point(2_174_114.28, 1_390_079.77))
    buffer = geom.buffer(1000)
    cursor.insertRow([buffer, "ZZ"])

print("Skript úspěšně končil.")
