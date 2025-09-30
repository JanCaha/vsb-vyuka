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

# korektní ukončení QGIS ale není vhodné volat samostatně, dojde k tomu automaticky
# manuální ukončení vypíše do konzole chybu "segmentation fault (core dumped)" - což není výrazný problém, ale lepší se tomu vyhnout
# qgis.exitQgis()
