from qgis.core import QgsApplication, QgsRasterFileWriter, QgsRasterIterator, QgsRasterLayer
from utils import data_path

qgis = QgsApplication([], False)
qgis.initQgis()

file = data_path("nahodny_raster.tif")

# změna názvu souboru, zachováme příponu
new_file = file.with_stem("novy_raster")

raster_layer = QgsRasterLayer(file.as_posix(), "nahodný raster", "gdal")

#  rastr writer pro tvorbu rastru, použijeme GDAL provider a formát určíme podle přípony souboru
writer = QgsRasterFileWriter(new_file.as_posix())
writer.setOutputProviderKey("gdal")
writer.setOutputFormat(QgsRasterFileWriter.driverForExtension(new_file.suffix))

# vytvoříme rastr z jedním pásmem a údaji dle původního rastru
new_raster_dp = writer.createOneBandRaster(
    raster_layer.dataProvider().dataType(1),
    raster_layer.width(),
    raster_layer.height(),
    raster_layer.extent(),
    raster_layer.crs(),
)

# iterátor
raster_iterator = QgsRasterIterator(raster_layer.dataProvider())
raster_iterator.setMaximumTileHeight(100)
raster_iterator.setMaximumTileWidth(100)

raster_iterator.startRasterRead(1, raster_layer.width(), raster_layer.height(), raster_layer.extent())

returned, columns, rows, block, top_left_x, top_left_y = raster_iterator.readNextRasterPart(1)

# editace nového rastru
new_raster_dp.setEditable(True)

count = 0
while returned:
    # zápis bloku do nového rastru - v podstatě kopírování
    new_raster_dp.writeBlock(block, 1, top_left_x, top_left_y)

    # další blok rastru pro cyklus
    returned, columns, rows, block, top_left_x, top_left_y = raster_iterator.readNextRasterPart(1)
