from qgis.core import QgsApplication, QgsRasterIterator, QgsRasterLayer, QgsRectangle
from utils import data_path

qgis = QgsApplication([], False)
qgis.initQgis()

raster_layer = QgsRasterLayer(data_path("nahodny_raster_upravy.tif").as_posix(), "nahodný raster", "gdal")

raster_layer_dp = raster_layer.dataProvider()

raster_iterator = QgsRasterIterator(raster_layer_dp)
raster_iterator.setMaximumTileHeight(100)
raster_iterator.setMaximumTileWidth(100)

raster_iterator.startRasterRead(1, raster_layer.width(), raster_layer.height(), raster_layer.extent())

returned, columns, rows, block, top_left_x, top_left_y = raster_iterator.readNextRasterPart(1)

# nastavení editace rastru
raster_layer_dp.setEditable(True)

count = 0
while returned:

    # úprava vybraných hodot v bloku - nastavení na NoData
    for i in range(block.width() * block.height()):
        value = block.value(i)
        if value > 50:
            block.setValue(i, block.noDataValue())

    # zápis bloku zpět do rastru do lokace s daným odsazením
    raster_layer_dp.writeBlock(block, 1, top_left_x, top_left_y)

    print(f"{count} - {block.width()} : {block.height()}")
    count += 1

    # další blok rastru pro cyklus
    returned, columns, rows, block, top_left_x, top_left_y = raster_iterator.readNextRasterPart(1)

qgis.exitQgis()
