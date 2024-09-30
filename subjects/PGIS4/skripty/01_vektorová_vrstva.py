from qgis.core import QgsApplication, QgsFeature, QgsVectorLayer

# incializace QGIS a jeho kompoment
qgis = QgsApplication([], False)
qgis.initQgis()

layer = QgsVectorLayer("data/world.gpkg", "World", "ogr")

print(layer.id())
print(layer.name())
print(layer.crs())
print(layer.featureCount())

feature: QgsFeature
for feature in layer.getFeatures():
    print(feature.attributes())
    geom = feature.geometry().centroid()
    print(geom.asWkt())
    print("*" * 50)

# korektní ukončení QGIS
qgis.exitQgis()
