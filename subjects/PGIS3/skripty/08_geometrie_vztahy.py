import arcpy

# geometrie čtverce
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

# geometrie trojúhelníku
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

# výpis geometrie
print(rectangle.WKT)
print(triangle.WKT)

# kontroly shodnosti geometrií
print(rectangle == triangle)
print(rectangle != triangle)

# prostorové vztahy - průnik
intersect: arcpy.Geometry = rectangle.intersect(triangle, 1)
print(intersect.WKT)

# prostorové vztahy - sjednocení - dva způsoby zápisu jeden pomocí metody, druhý pomocí operátoru
union: arcpy.Geometry = rectangle.union(triangle)
union: arcpy.Geometry = rectangle | triangle
print(union.WKT)

# prostorové vztahy - rozdíl
difference: arcpy.Geometry = rectangle.difference(triangle)
print(difference.WKT)

# prostorové vztahy - symetrický rozdíl
symDiff: arcpy.Geometry = rectangle.symmetricDifference(triangle)
print(symDiff.WKT)
