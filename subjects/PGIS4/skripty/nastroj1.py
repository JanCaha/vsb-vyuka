from typing import Any, Optional

from qgis.core import (
    Qgis,
    QgsFeature,
    QgsFeatureRequest,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingException,
    QgsProcessingFeedback,
    QgsProcessingOutputNumber,
    QgsProcessingParameterExpression,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
)


class FilteredCentroidsProcessingAlgorithm(QgsProcessingAlgorithm):

    # textová id pro parametry nástroje
    INPUT = "INPUT"
    EXPRESSION = "EXPRESSION"
    OUTPUT = "OUTPUT"
    FEATURE_COUNT = "FEATURE_COUNT"

    # metodat pro tvorbu nástroje
    def createInstance(self):
        return FilteredCentroidsProcessingAlgorithm()

    # id nástroje
    def name(self) -> str:
        return "filteredcentroids"

    # název nástroje, jak se bude zobrazovat uživateli
    def displayName(self) -> str:
        return "Filtered Centroids"

    # kategorie nástroje, jak se bude zobrazovat uživateli
    def group(self) -> str:
        return "Example scripts"

    # id kategorie nástroje
    def groupId(self) -> str:
        return "examplescripts"

    # nápověda nástroje
    def shortHelpString(self) -> str:
        return "Example algorithm short description"

    # inicializace nástroje, parametry a jejich nastavení
    def initAlgorithm(self, config: Optional[dict[str, Any]] = None):

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input layer",
                [Qgis.ProcessingSourceType.VectorAnyGeometry],
            )
        )

        self.addParameter(
            QgsProcessingParameterExpression(
                self.EXPRESSION,
                "Filter",
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                "Output layer",
            )
        )

        self.addOutput(
            QgsProcessingOutputNumber(
                self.FEATURE_COUNT,
                "Feature count",
            )
        )

    # funkce spuštění nástroje
    def processAlgorithm(
        self,
        parameters: dict[str, Any],
        context: QgsProcessingContext,
        feedback: QgsProcessingFeedback,
    ) -> dict[str, Any]:

        # vstupní vrstva - načtení
        source = self.parameterAsSource(parameters, self.INPUT, context)

        # kontrola, že vrstva je ok
        if source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        # načtení výrazu
        expression = self.parameterAsExpression(
            parameters,
            self.EXPRESSION,
            context,
        )

        # vytvoření sinku (výstupní vektorové vrstvy) - dvě proměnné, samotný sink a jeho název pro načtení do QGIS
        sink, dest_id = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            source.fields(),
            Qgis.WkbType.Point,
            source.sourceCrs(),
        )

        # kontrola sinku, že je ok a případné ukončení, pokud není
        if sink is None:
            raise QgsProcessingException(
                self.invalidSinkError(
                    parameters,
                    self.OUTPUT,
                )
            )

        # info uživateli
        feedback.pushInfo("Vstupní parametry byly načteny")

        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # tvorba requestu na foltrování dat
        req = QgsFeatureRequest()
        req.setFilterExpression(expression)

        features = source.getFeatures(req)

        # iterace na prvky
        feature: QgsFeature
        for current, feature in enumerate(features):

            # kontrola, zda uživatel proces neukončil
            if feedback.isCanceled():
                break

            # tvorba nového prvku a vyplnění atributů a geometrie
            new_feature = QgsFeature(source.fields())
            new_feature.setGeometry(feature.geometry().centroid())
            new_feature.setAttributes(feature.attributes())

            # vložení prvku do sinku
            sink.addFeature(new_feature, QgsFeatureSink.Flag.FastInsert)

            # update progresu
            feedback.setProgress(int(current * total))

        # vrácení výstupních hodnot
        return {
            self.OUTPUT: dest_id,
            self.FEATURE_COUNT: current,
        }
