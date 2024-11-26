# no GA run
# skript pro spuštění z Python konzole QGIS

# importy teoreticky nejsou třeba, ale pro jistotu a srozumitelnost kódu je ponechávám
from qgis.core import Qgis, QgsMessageLog, QgsPointXY
from qgis.gui import QgisInterface, QgsMapCanvas, QgsMapMouseEvent, QgsMapToolEdit, QgsRubberBand
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QAction

# iface je globální proměnná, která je dostupná v konzoli QGIS
iface: QgisInterface


# třída pro kreslení polygonu, odvozená od nástroje pro editaci
class DrawPoly(QgsMapToolEdit):

    def __init__(self, canvas: QgsMapCanvas):
        super().__init__(canvas)

        # rubber band je speciální třída pro kreslení geometrie do mapového okna
        self._rubber_band = self.createRubberBand(Qgis.GeometryType.Polygon)
        # nastavení barvy kreslení
        self._rubber_band.setFillColor(QColor(0, 255, 0))

        # nastavení prvního bodu nástroje - pomáhá identifikovat, jak se nástroj používá
        self._first_point = None

    # aktivace nástroje, zde se nastaví kurzor a zobrazí se rubber band
    def activate(self):
        self._rubber_band.show()
        self.canvas().setCursor(Qt.CursorShape.CrossCursor)
        self._first_point = None
        super().activate()

    # při deaktivaci všeechno zrušíme nastavíme do výchozího stavu
    def deactivate(self):
        self.canvas().setCursor(Qt.CursorShape.ArrowCursor)
        self._rubber_band.reset(Qgis.GeometryType.Polygon)
        self._fist_point = None
        return super().deactivate()

    # metoda pro zachycení události pohybu myši
    def canvasMoveEvent(self, e: QgsMapMouseEvent):
        # pokud existuje první bod, tak odstraníme předchozí bod a přidáme nový
        # tím se odstraní poslední bod vzniklý pohybem myši a přidá se nový
        if self._first_point:
            if self._rubber_band.numberOfVertices() > 1:
                self._rubber_band.removeLastPoint()
            self._rubber_band.addPoint(e.mapPoint())
        return super().canvasMoveEvent(e)

    # metoda pro zachycení události kliku myši, zachytáváme puštění tlačítka uživatelem
    def canvasReleaseEvent(self, e: QgsMapMouseEvent):
        # leve tlačítko přídává bod do polygonu (rubber band)
        if e.button() == Qt.LeftButton:
            if self._first_point is None:
                self._first_point = e.mapPoint()
            self._rubber_band.addPoint(e.mapPoint())
        # pravé tlačítko ukončuje kreslení a vypíše WKT do logu QGIS
        elif e.button() == Qt.RightButton:
            QgsMessageLog.logMessage(f"WKT: {self._rubber_band.asGeometry().asWkt()}")
            self.deactivate()


# nástroj vytvoříme a uložíme do proměnné
tool = DrawPoly(iface.mapCanvas())


# funkce pro aktivaci nástroje, iface a tool jsou zde globální proměnné (neměly by se používat, ale zde je to jednodušší)
def activate_tool():
    # funkce deaktivace nástroje - používá signál pro deaktivaci, pokročilá technika GUI
    tool.deactivated.connect(lambda: iface.mapCanvas().unsetMapTool(tool))
    # nastavení nástroje do mapového okna
    iface.mapCanvas().setMapTool(tool)


# vytvoření tlačítka v GUI pro aktivaci nástroje
action = QAction("tool", iface.mainWindow())
# po klinutí na tlačítko se zavolá funkce activate_tool
action.triggered.connect(activate_tool)
# přidání tlačítka do toolbaru
iface.addToolBarIcon(action)
