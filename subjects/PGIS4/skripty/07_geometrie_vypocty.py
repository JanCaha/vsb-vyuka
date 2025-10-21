from qgis.core import (
    QgsApplication,
    QgsCoordinateReferenceSystem,
    QgsDistanceArea,
    QgsGeometry,
    QgsPointXY,
    QgsProject,
    QgsUnitTypes,
)

qgis = QgsApplication([], False)
qgis.initQgis()

# Vytvoření polygonu (čtverec 100x100 m v S-JTSK)
points = [
    QgsPointXY(-870000, -1090000),
    QgsPointXY(-870000, -1090100),
    QgsPointXY(-870100, -1090100),
    QgsPointXY(-870100, -1090000),
    QgsPointXY(-870000, -1090000),
]

geom = QgsGeometry.fromPolygonXY([points])

print(f"Obvod: {geom.length():.2f}")
print(f"Plocha: {geom.area():.2f}")

# Inicializace výpočtové třídy
d = QgsDistanceArea()
# set S-JTSK
d.setSourceCrs(
    QgsCoordinateReferenceSystem("EPSG:5514"),
    QgsProject.instance().transformContext(),
)

# --------------------------------------
# elipsoid WGS84
d.setEllipsoid("GRS80")

# Výpočet obvodu a plochy
perimeter = d.measurePerimeter(geom)
area = d.measureArea(geom)

print(f"Obvod: {perimeter:.2f} {QgsUnitTypes.toString(d.lengthUnits())}")
print(f"Plocha: {area:.2f} {QgsUnitTypes.toString(d.areaUnits())}")

# --------------------------------------
# změna elipsoidu na Bessel 1841 - ten patří k S-JTSK
d.setEllipsoid("Bessel 1841")

# Výpočet obvodu a plochy
perimeter = d.measurePerimeter(geom)
area = d.measureArea(geom)

print(f"Obvod: {perimeter:.2f} {QgsUnitTypes.toString(d.lengthUnits())}")
print(f"Plocha: {area:.2f} {QgsUnitTypes.toString(d.areaUnits())}")
