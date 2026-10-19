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

# Definice souřadnicového systému S-JTSK (EPSG:5514)
sjtsk = QgsCoordinateReferenceSystem("EPSG:5514")
# Inicializace výpočtové třídy
d = QgsDistanceArea()
# set S-JTSK
d.setSourceCrs(
    sjtsk,
    QgsProject.instance().transformContext(),
)

# --------------------------------------
# elipsoid WGS84
print(f"=== Elipsoid: {sjtsk.ellipsoidAcronym()} ===")
d.setEllipsoid(sjtsk.ellipsoidAcronym())

# Výpočet obvodu a plochy
perimeter = d.measurePerimeter(geom)
area = d.measureArea(geom)

print(f"Obvod: {perimeter:.2f} {QgsUnitTypes.toString(d.lengthUnits())}")
print(f"Plocha: {area:.2f} {QgsUnitTypes.toString(d.areaUnits())}")

# --------------------------------------
# změna elipsoidu na GRS80
ellipsoid = "GRS80"
print(f"=== Elipsoid: {ellipsoid} ===")
d.setEllipsoid(ellipsoid)

# Výpočet obvodu a plochy
perimeter = d.measurePerimeter(geom)
area = d.measureArea(geom)

print(f"Obvod: {perimeter:.2f} {QgsUnitTypes.toString(d.lengthUnits())}")
print(f"Plocha: {area:.2f} {QgsUnitTypes.toString(d.areaUnits())}")
