import arcpy

crs_wgs84 = arcpy.SpatialReference(4326)
crs_sjtsk = arcpy.SpatialReference(5514)

point = arcpy.PointGeometry(
    arcpy.Point(18.1647269, 49.8344128),
    crs_wgs84,
)

print(point.WKT)

point_sjtsk = point.projectAs(crs_sjtsk)

print(point_sjtsk.WKT)
