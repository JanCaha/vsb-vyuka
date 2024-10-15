from qgis.core import QgsGeometry, QgsPoint, QgsPointXY

# geometrie dvou polygonu
rectangle = QgsGeometry.fromPolygonXY(
    [
        [
            QgsPointXY(0, 0),
            QgsPointXY(1, 0),
            QgsPointXY(1, 1),
            QgsPointXY(0, 1),
        ]
    ]
)

triangle = QgsGeometry.fromPolygonXY(
    [
        [
            QgsPointXY(0.5, -0.5),
            QgsPointXY(0.5, 1.5),
            QgsPointXY(1.2, 0.5),
        ]
    ]
)

# WKT pro zobrazování
print(rectangle.asWkt())
print("-" * 10)
print(triangle.asWkt())
print("-" * 10)

# geometrické vztahy polygonů
intersect = rectangle.intersection(triangle)
print(intersect.asWkt())
print("-" * 10)

difference = rectangle.difference(triangle)
print(difference.asWkt())
print("-" * 10)

# práce s vrcholy polygonu
sym_difference = rectangle.symDifference(triangle)
sym_difference.moveVertex(-5, -5, 0)
sym_difference.moveVertex(-3, -3, 1)
sym_difference.deleteVertex(8)

print(sym_difference.asWkt())
print("-" * 10)

# iterace přes vrcholy a úprava některých z nich podle podmínky
vertex: QgsPoint
for i, vertex in enumerate(sym_difference.vertices()):
    print(f"{i} - {vertex}")
    if vertex.x() > 0.75:
        sym_difference.moveVertex(vertex.x() - 0.15, vertex.y(), i)

print(sym_difference.asWkt())
