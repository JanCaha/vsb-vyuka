import arcpy
import utils

crs_wgs84 = arcpy.SpatialReference(4326)
crs_sjtsk = arcpy.SpatialReference(5514)

# informace o souřadnicových systémech
print(f"{crs_wgs84.type}: {crs_wgs84.angularUnitName} - {crs_wgs84.linearUnitName}")
print(f"{crs_sjtsk.type}: {crs_sjtsk.angularUnitName} - {crs_sjtsk.linearUnitName}")

print(utils.is_projected(crs_wgs84))
print(utils.is_projected(crs_sjtsk))

line = arcpy.Polyline(
    arcpy.Array(
        [
            arcpy.Point(18.164_726_9, 49.834_412_8),
            arcpy.Point(12.190_417_5, 50.221_635_6),
        ]
    ),
    crs_wgs84,
)

# délka v WGS84 nedává smysl - úhlové jednotky
print(line.WKT)
print(line.length)

line_sjtsk: arcpy.Geometry = line.projectAs(crs_sjtsk)

# délka v S-JTSK dává smysl - metry, vyděleno 1000 pro km
print(line_sjtsk.WKT)
print(line_sjtsk.length / 1000)
