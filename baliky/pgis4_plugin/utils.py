from qgis.core import Qgis, QgsFeature, QgsField, QgsGeometry
from qgis.PyQt.QtCore import QVariant


def convert_to_point_no_lines(feature: QgsFeature) -> QgsFeature:
    if feature.geometry().wkbType() == Qgis.WkbType.LineString:
        raise ValueError("Nepracuju s liniemi!")

    return convert_to_point(feature)


def convert_to_point(feature: QgsFeature) -> QgsFeature:
    fields = feature.fields()
    fields.append(QgsField("x", QVariant.Type.Double))
    fields.append(QgsField("y", QVariant.Type.Double))

    new_feature = QgsFeature(fields)

    attributes = []
    for field in feature.fields().names():
        attributes.append(feature.attribute(field))

    geom = feature.geometry().centroid()

    attributes.append(geom.asPoint().x())
    attributes.append(geom.asPoint().y())

    new_feature.setAttributes(attributes)
    new_feature.setGeometry(geom)

    return new_feature
