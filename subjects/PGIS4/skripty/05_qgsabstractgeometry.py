# dílčí třídy QgsAbstractGeometry rozhraní
from qgis.core import QgsGeometry, QgsPoint, QgsTriangle

# QgsAbstractGeometry interface - implementovaný v třídě QgsTriangle
triangle = QgsTriangle(
    QgsPoint(0, 0),
    QgsPoint(1, 0),
    QgsPoint(0.5, 2),
)

print(triangle)
print(triangle.area())
print(triangle.length())

# QgsAbstractGeometry interface - implementovaný v třídě QgsPoint
p = QgsPoint(0, 0)
print(p)
print(p.area())
print(p.length())
print(p.partCount())
print(p.ringCount())

# QgsGeometry hlavní třídy, v níž existuje QgsAbstractGeometry jako její součást
geom = QgsGeometry(triangle)
print(geom)

# densifikace geometrie
geom_densified = geom.densifyByDistance(0.3)

print(geom_densified)
print(geom_densified.asWkt())
