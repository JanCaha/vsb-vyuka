from qgis.core import QgsProcessingProvider

from .nastroj1 import PolygonAreaClassificationAlgorithm
from .nastroj2 import RasterThresholdClassificationAlgorithm


class Pgis4ProcessingProvider(QgsProcessingProvider):

    # funkce načtení
    def load(self) -> bool:
        self.refreshAlgorithms()

        return True

    # připravení všech algoritmů
    def loadAlgorithms(self):
        self.addAlgorithm(PolygonAreaClassificationAlgorithm())
        self.addAlgorithm(RasterThresholdClassificationAlgorithm())

    def id(self):
        return "pgis4_processing"

    def name(self):
        return "PGIS4 Processing"
