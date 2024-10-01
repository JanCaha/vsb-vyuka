from qgis.core import QgsApplication, QgsFeature, QgsVectorLayer
from utils import data_path

# incializace QGIS a jeho kompoment
qgis = QgsApplication([], False)
qgis.initQgis()

layer = QgsVectorLayer(data_path("world.gpkg").as_posix(), "World", "ogr")

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
