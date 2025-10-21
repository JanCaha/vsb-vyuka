import math

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

print("===WKT===")
# výpis geometrie
print(rectangle.WKT)
print(triangle.WKT)

print("===Shodnost/Neshodnost===")
# kontroly shodnosti geometrií
print(rectangle == triangle)
print(rectangle != triangle)

print("===Průnik===")
# prostorové vztahy - průnik
intersect: arcpy.Geometry = rectangle.intersect(triangle, 4)
print(intersect.WKT)

print("===Sjednocení===")
# prostorové vztahy - sjednocení - dva způsoby zápisu jeden pomocí metody, druhý pomocí operátoru
union: arcpy.Geometry = rectangle.union(triangle)
# union: arcpy.Geometry = rectangle | triangle
print(union.WKT)

print("===Rozdíl===")
# prostorové vztahy - rozdíl
difference: arcpy.Geometry = rectangle.difference(triangle)
print(difference.WKT)

print("===Symetrický Rozdíl===")
# prostorové vztahy - symetrický rozdíl
symDiff: arcpy.Geometry = rectangle.symmetricDifference(triangle)
print(symDiff.WKT)

print("===Rotace kolem 0,0===")
rotate1: arcpy.Geometry = rectangle.rotate(rotation_angle=math.radians(90))
print(rotate1.WKT)

print("===Rotace kolem 0.5,0.5===")
rotate2: arcpy.Geometry = rectangle.rotate(arcpy.Point(0.5, 0.5), rotation_angle=math.radians(45))
print(rotate2.WKT)

print("===Zmenšení kolem 0,0===")
scale1: arcpy.Geometry = rectangle.scale(sx=0.5, sy=0.5)
print(scale1.WKT)

print("===Zmenšení kolem 0.5,0.5===")
scale2: arcpy.Geometry = rectangle.scale(arcpy.Point(0.5, 0.5), sx=0.5, sy=0.5)
print(scale2.WKT)
