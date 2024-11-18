import typing

from qgis import processing
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
)


class ExampleMultiStepProcessingAlgorithm(QgsProcessingAlgorithm):

    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def createInstance(self):
        return ExampleMultiStepProcessingAlgorithm()

    def name(self):
        return "examplemultistepalgorithm"

    def displayName(self):
        return "Example multistep algorithm"

    def group(self):
        return "Example scripts"

    def groupId(self):
        return "examplescripts"

    def shortHelpString(self):
        return "Example multistep algorithm "

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT, "Input layer", [QgsProcessing.SourceType.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, "Output layer"))

    def checkParameterValues(self, parameters, context) -> typing.Tuple[bool, str]:
        # v této funkci můžeme provádět kontrolu parametrů

        # parametry musíme načíst jako při zpracování algoritmu - skrze funkce self.parameterAs...
        vector_layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)

        # kontrola
        if vector_layer is not None:
            if vector_layer.crs().isGeographic():
                # pokud kontrola neprojde vracíme FALSE and chybovou hlášku
                return False, "Input layer must be projected"

        return super().checkParameterValues(parameters, context)

    def processAlgorithm(self, parameters, context, feedback) -> typing.Dict[str, typing.Any]:

        # vícekrokový feedback pro zobrazení průběhu zpracování
        feedback = QgsProcessingMultiStepFeedback(3, feedback)

        vector_layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)

        if vector_layer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        # spuštění dílčího algoritmu - předáváme context a feedback, aby algoritm mohl zobrazovat průběh
        # nastavíme is_child_algorithm=True, aby bylo jasné že algoritmus je součástí jiného algoritmu
        result = processing.run(  # pylint: disable=assignment-from-no-return
            "native:centroids",
            {
                "INPUT": vector_layer,
                "ALL_PARTS": False,
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        # krok hotový
        feedback.setCurrentStep(1)
        # kontrola jestli uživatel nezrušil zpracování
        if feedback.isCanceled():
            return {}

        # INPUT pro další krok je výstup z předchozího kroku - result["OUTPUT"]
        result = processing.run(  # pylint: disable=assignment-from-no-return
            "native:buffer",
            {
                "INPUT": result["OUTPUT"],
                "DISTANCE": 1000_000,
                "SEGMENTS": 5,
                "END_CAP_STYLE": 0,
                "JOIN_STYLE": 0,
                "MITER_LIMIT": 2,
                "DISSOLVE": False,
                "SEPARATE_DISJOINT": False,
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        result = processing.run(  # pylint: disable=assignment-from-no-return
            "native:dissolve",
            {
                "INPUT": result["OUTPUT"],
                "FIELD": [],
                "SEPARATE_DISJOINT": False,
                "OUTPUT": parameters["OUTPUT"],
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )  # pylint: disable=assignment-from-no-return

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # návratová hodnota
        return {self.OUTPUT: result["OUTPUT"]}
