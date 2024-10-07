# ukázka výběru prvků pomocí QgsFeatureRequest

from qgis.core import QgsApplication, QgsFeature, QgsFeatureRequest, QgsRectangle, QgsVectorLayer

qgis = QgsApplication([], False)
qgis.initQgis()

layer = QgsVectorLayer("data/world.gpkg", "World", "ogr")

# zájmové území
rectangle = QgsRectangle(0, 45, 20, 55)

# filtr hodnot
expression = " \"NAME\" LIKE '%a%' "

# vytvoření objektu pro výběr prvků
feature_req = QgsFeatureRequest()
feature_req.setFilterRect(rectangle)
feature_req.setFilterExpression(expression)

# settřídění prvků
clause = QgsFeatureRequest.OrderByClause("Name", ascending=False)
order_by = QgsFeatureRequest.OrderBy([clause])

feature_req.setOrderBy(order_by)

feature: QgsFeature
for feature in layer.getFeatures(feature_req):
    print(feature.attributes())

qgis.exitQgis()
