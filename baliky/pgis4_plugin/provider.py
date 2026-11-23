from qgis.core import QgsProcessingProvider

from .nastroj1 import Nastroj1
from .nastroj2 import Nastroj2


class MujProvider(QgsProcessingProvider):

    # funkce načtení
    def load(self) -> bool:
        self.refreshAlgorithms()

        return True

    # připravení všech algoritmů
    def loadAlgorithms(self):
        self.addAlgorithm(Nastroj1())
        self.addAlgorithm(Nastroj2())

    def id(self):
        return "mujprovider"

    def name(self):
        return "Můj Provider"
