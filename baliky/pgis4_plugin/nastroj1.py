import processing
from qgis.core import (
    QgsFeature,
    QgsField,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
)
from qgis.PyQt.QtCore import QVariant


class Nastroj1(QgsProcessingAlgorithm):
    INPUT = "vstupni_vrstva"
    OUTPUT = "vystupni_vrstva"
    NUMERICALLIMIT = "ciselny_limit"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT, "Vstupní vrstva", types=[QgsProcessing.TypeVectorPolygon], defaultValue=None
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.NUMERICALLIMIT,
                "Limitní hodnota",
                QgsProcessingParameterNumber.Type.Double,
                defaultValue=80000 * 1000,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                "Výsledná vrstva",
                type=QgsProcessing.TypeVectorAnyGeometry,
                createByDefault=True,
                defaultValue=None,
            )
        )

    def checkParameterValues(self, parameters, context):
        vstupni_vrstva = self.parameterAsVectorLayer(
            parameters,
            self.INPUT,
            context,
        )

        crs = vstupni_vrstva.crs()

        if crs.isGeographic():
            return False, "Souřadnicový systém vrstvy nesmí být geografický."

        if "Moje_Pole" not in vstupni_vrstva.fields().names():
            return False, "Moje_Pole musí existovat mezi atributy."

        return super().checkParameterValues(parameters, context)

    def processAlgorithm(self, parameters, context, model_feedback):
        vstupni_vrstva = self.parameterAsVectorLayer(
            parameters,
            self.INPUT,
            context,
        )

        if vstupni_vrstva is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        ciselny_limit = self.parameterAsDouble(
            parameters,
            self.NUMERICALLIMIT,
            context,
        )

        fields = vstupni_vrstva.fields()
        fields.append(
            QgsField(
                "Rozloha",
                QVariant.Type.Double,
            )
        )
        fields.append(
            QgsField(
                "Vetsi_nez_limit",
                QVariant.Type.Bool,
            )
        )

        vystupni_vrstva, umisteni_souboru = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields=fields,
            geometryType=vstupni_vrstva.wkbType(),
            crs=vstupni_vrstva.crs(),
        )

        if vystupni_vrstva is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        for feature in vstupni_vrstva.getFeatures():
            new_feature = QgsFeature(fields)
            new_feature.setGeometry(feature.geometry().centroid().buffer(0.5, 6))

            rozloha = feature.geometry().area()

            atributy = feature.attributes()
            atributy.append(rozloha)
            atributy.append(rozloha > ciselny_limit)

            new_feature.setAttributes(atributy)

            vystupni_vrstva.addFeature(new_feature)

        return {self.OUTPUT: vystupni_vrstva}

    def name(self):
        return "Kategorizace dle rozlohy"

    def displayName(self):
        return "Kategorizace dle rozlohy"

    def group(self):
        return "Zkouška"

    def groupId(self):
        return "Zkouška"

    def createInstance(self):
        return Nastroj1()
