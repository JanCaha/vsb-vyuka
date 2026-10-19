# dílčí třídy QgsAbstractGeometry rozhraní
from qgis.core import QgsGeometry, QgsPoint, QgsTriangle

# QgsAbstractGeometry interface - implementovaný v třídě QgsTriangle
triangle = QgsTriangle(
    QgsPoint(0, 0),
    QgsPoint(1, 0),
    QgsPoint(0.5, 2),
)

print(f"Objekt: {triangle}")
print(f"Rozloha: {triangle.area()}")
print(f"Obvod: {triangle.length()}")

# QgsAbstractGeometry interface - implementovaný v třídě QgsPoint
p = QgsPoint(0, 0)
print(f"Objekt: {p}")
print(f"Rozloha: {p.area()}")
print(f"Obvod: {p.length()}")
print(f"Počet částí: {p.partCount()}")
print(f"Počet prstenců: {p.ringCount()}")

# QgsGeometry hlavní třídy, v níž existuje QgsAbstractGeometry jako její součást
geom = QgsGeometry(triangle)
print(f"Geometrie: {geom}")

# densifikace geometrie
geom_densified = geom.densifyByDistance(0.3)

print(f"Densifikovaná geometrie: {geom_densified}")
print(f"Densifikovaná geometrie WKT: {geom_densified.asWkt()}")
