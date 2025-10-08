# ukázka výběru prvků pomocí QgsFeatureRequest

from qgis.core import QgsApplication, QgsFeature, QgsFeatureRequest, QgsRectangle, QgsVectorLayer
from utils import data_path

qgis = QgsApplication([], False)
qgis.initQgis()

layer_path = data_path("world.gpkg").as_posix()
# cesta_k_souboru|layername=jmeno_vrstvy
layer = QgsVectorLayer(f"{layer_path}|layername=countries", "World", "ogr")

# zájmové území
rectangle = QgsRectangle(0, 45, 20, 55)

# filtr hodnot
expression = " \"NAME\" LIKE '%u%' "

# vytvoření objektu pro výběr prvků
feature_req = QgsFeatureRequest()
feature_req.setFilterRect(rectangle)
feature_req.setFilterExpression(expression)

# setřídění prvků
clause = QgsFeatureRequest.OrderByClause("Name", ascending=False)
order_by = QgsFeatureRequest.OrderBy([clause])

# aplikace setřídění do požadavku
feature_req.setOrderBy(order_by)

# průchod vybranými prvky
feature: QgsFeature
for feature in layer.getFeatures(feature_req):
    print(feature.attributes())
