from pprint import pprint

import arcpy
import utils

utils.setup_env("ProgrammingPro/Databases/Trippville_GIS.gdb")

feature_class = "Wetlands"
new_layer = "Copy_of_Wetlands"

# popis objektu jako python slovník - viz dole přístup k hodnotám
desc = arcpy.da.Describe(feature_class)
# pprint(desc)

arcpy.management.CreateFeatureclass(
    arcpy.env.workspace,
    new_layer,
    template=feature_class,
    geometry_type=desc["shapeType"],
    spatial_reference=desc["spatialReference"],
)

feature_count = 0

# kurzor na průchod daty
with arcpy.da.SearchCursor(
    feature_class,
    [
        "OID@",
        "SHAPE@",
        "SHAPE@AREA",
        "WATER1",
        "NWI_CODE",
    ],
) as search_cursor:

    # kurzor na vkládání dat
    with arcpy.da.InsertCursor(new_layer, ["SHAPE@", "WATER1", "NWI_CODE", "PLAN_CODE"]) as insert_cursor:

        # řádky pro procházená data
        for row in search_cursor:

            # podmínka na sloupci SHAPE@AREA - viz kurzor na průchod daty
            if row[2] > 900_000:

                # kurzor na vkládání dat
                insert_cursor.insertRow([row[1], row[3], row[4], "--"])
                feature_count += 1

print(f"Bylo vloženo {feature_count} prvků.")

# kurzor na úpravu/mazání dat
with arcpy.da.UpdateCursor(new_layer, ["OID@"], where_clause="WATER1 = 'C'") as update_cursor:
    for row in update_cursor:
        update_cursor.deleteRow()

# nový popis objektu
desc_new = arcpy.da.Describe(new_layer)
pprint(desc_new)
