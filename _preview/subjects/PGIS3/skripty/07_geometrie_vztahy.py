import arcpy

rectangle = arcpy.Polygon(
    arcpy.Array(
        [
            arcpy.Point(0, 0),
            arcpy.Point(1, 0),
            arcpy.Point(1, 1),
            arcpy.Point(0, 1),
            arcpy.Point(0, 0),
        ]
    )
)

triangle = arcpy.Polygon(
    arcpy.Array(
        [
            arcpy.Point(0.5, -0.5),
            arcpy.Point(0.5, 1.5),
            arcpy.Point(1.2, 0.5),
            arcpy.Point(0.5, -0.5),
        ]
    )
)

print(rectangle.WKT)
print(triangle.WKT)

print(rectangle == triangle)
print(rectangle != triangle)

intersect: arcpy.Geometry = rectangle.intersect(triangle, 1)
print(intersect.WKT)

union: arcpy.Geometry = rectangle.union(triangle)
union: arcpy.Geometry = rectangle | triangle
print(union.WKT)

difference: arcpy.Geometry = rectangle.difference(triangle)
print(difference.WKT)

symDiff: arcpy.Geometry = rectangle.symmetricDifference(triangle)
print(symDiff.WKT)
