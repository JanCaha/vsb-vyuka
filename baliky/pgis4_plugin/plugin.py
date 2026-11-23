from qgis.core import QgsApplication
from qgis.gui import QgisInterface

from .provider import Pgis4ProcessingProvider


class MujPlugin:

    # inicializace proměnných
    def __init__(self, iface: QgisInterface):
        self.iface: QgisInterface = iface

        self.provider = Pgis4ProcessingProvider()

        # načtení provideru do QGIS registru
        QgsApplication.processingRegistry().addProvider(self.provider)

    # při vypnutí pluginu korektně odpojit providera
    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)

    # inicializace GUI - zde žádné nemáme
    def initGui(self):
        pass
