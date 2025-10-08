import typing

from qgis.core import (
    Qgis,
    QgsApplication,
    QgsCoordinateTransformContext,
    QgsFeature,
    QgsFeatureRequest,
    QgsField,
    QgsMemoryProviderUtils,
    QgsPoint,
    QgsRectangle,
    QgsTriangle,
    QgsVectorFileWriter,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QMetaType
from utils import data_path, save_data_path

qgis = QgsApplication([], False)
qgis.initQgis()

layer_path = data_path("world.gpkg").as_posix()
# cesta_k_souboru|layername=jmeno_vrstvy
layer = QgsVectorLayer(f"{layer_path}|layername=countries", "World", "ogr")
layer = typing.cast(QgsVectorLayer, layer)

rectangle = QgsRectangle(0, 45, 20, 55)
expression = " \"NAME\" LIKE '%a%' "

feature_req = QgsFeatureRequest()
feature_req.setFilterRect(rectangle)
feature_req.setFilterExpression(expression)

clause = QgsFeatureRequest.OrderByClause("Name", ascending=False)
order_by = QgsFeatureRequest.OrderBy([clause])

feature_req.setOrderBy(order_by)

# úprava atributů přidáním nového pole
fields = layer.fields()
fields.append(
    QgsField(
        "moje_pole",
        QMetaType.Type.Double,
    )
)

# vytvoření vrstvy v paměti
memory_layer = QgsMemoryProviderUtils.createMemoryLayer(
    name="filtered",
    fields=fields,
    geometryType=Qgis.WkbType.Polygon,
    crs=layer.crs(),
)
memory_layer = typing.cast(QgsVectorLayer, memory_layer)

print(memory_layer.featureCount())

# zapnutí editace vrstvy
memory_layer.startEditing()

feature: QgsFeature
for feature in layer.getFeatures(feature_req):
    new_feature = QgsFeature(fields)

    # kopirování atributů z původního prvku do nového
    old_field: QgsField
    for old_field in feature.fields():
        old_field_name = old_field.name()
        value = feature.attribute(old_field_name)
        new_feature.setAttribute(
            old_field_name,
            value,
        )

    # tvorba geometrie trojúhelníku
    point = feature.geometry().centroid().asPoint()
    triangle = QgsTriangle(
        QgsPoint(point.x() - 1, point.y()),
        QgsPoint(point.x() + 1, point.y()),
        QgsPoint(point.x(), point.y() + 1),
    )
    new_feature.setGeometry(triangle)

    # nastavení atrbutu nového pole
    new_feature.setAttribute("moje_pole", 0.5)

    # vložení nového prvku do vrstvy skrze data provider
    memory_layer.dataProvider().addFeature(new_feature)

# uložení provedených změn
memory_layer.commitChanges()

print(memory_layer.featureCount())

# nastavení možností pro uložení vrstvy
options = QgsVectorFileWriter.SaveVectorOptions()
options.actionOnExistingFile = QgsVectorFileWriter.ActionOnExistingFile.CreateOrOverwriteFile

# cesta k uložení souboru s vrstvou
file_path = save_data_path(f"{memory_layer.name()}.gpkg", delete_if_exist=True).as_posix()

# uložení vrstvy do souboru
QgsVectorFileWriter.writeAsVectorFormatV3(
    memory_layer,
    file_path,
    QgsCoordinateTransformContext(),
    options,
)
