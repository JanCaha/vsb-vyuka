# předpokládáme existenci souboru s projektem
from qgis.core import (
    Qgis,
    QgsApplication,
    QgsLayoutExporter,
    QgsLayoutItemLabel,
    QgsLayoutItemScaleBar,
    QgsLayoutPoint,
    QgsPrintLayout,
    QgsProject,
)
from qgis.PyQt.QtGui import QColor
from utils import data_path, save_data_path

qgis = QgsApplication([], False)
qgis.initQgis()

# vytvoření instance projektu a načtení ze souboru
project = QgsProject.instance()
open = project.read(data_path(r"projekt1.qgz").as_posix())
# open by měl být TRUE, pokud se projekt načetl správně
print(open)

# vlastnosti projektu
print(f"Vrstvy: {project.mapLayers()}")
print(f"Crs projektu: {project.crs()}")
print(f"Poslední editace: {project.lastModified()}")
print(f"Jednotky měření: {project.distanceUnits()}")

# změna názvu projektu
print("---")
print(f"Původní název: {project.title()}")
project.setTitle("Můj projekt")
print(f"Nový název: {project.title()}")

# uložení vlastních proměnných do projektu
project.setCustomVariables({"my_data": 123456})
data = project.customVariables()["my_data"]
print(data)

# projektu uložíme buď se změnami nebo do nového souboru
# project.write()
# project.write(r"C:\Users\cah0021\Documents\projekt2.qgz")

# layout manager pro práci s layouty
layout_manager = project.layoutManager()

# extrakce layout podle jeho názvu
layout: QgsPrintLayout = layout_manager.layoutByName("Layout 1")
# pokud layout najdeme bude mít proměnná hodnotu, jinak None
print(layout)

# extrakce komponenty layout podle jejího ID
item: QgsLayoutItemScaleBar = layout.itemById("ScaleBar1")
# změna nastavení prvku
item.attemptMove(
    QgsLayoutPoint(
        10,
        10,
        Qgis.LayoutUnit.Centimeters,
    )
)
item.setUnits(Qgis.DistanceUnit.Miles)
item.setUnitLabel("Miles")

# extrakce komponenty layout podle jejího ID
item_1: QgsLayoutItemLabel = layout.itemById("Text1")

# změna textu
item_1.setText("Nějaký nový text")

# extrakce fomátování textu, jeho úprava - změna barvy a velikosti
text_format = item_1.textFormat()
# QColor("#ff0000")
text_format.setColor(QColor(255, 0, 0))
text_format.setSize(25)
# vložení formátu se změnami zpět
item_1.setTextFormat(text_format)

# rotace textu
item_1.setItemRotation(90)

# export layoutu do PDF
exporter = QgsLayoutExporter(layout)
options = QgsLayoutExporter.PdfExportSettings()
options.forceVectorOutput = True
exporter.exportToPdf(save_data_path("layout_exported.pdf").as_posix(), options)

# uložení změn
project.write()
