from qgis.core import QgsApplication, QgsRasterIterator, QgsRasterLayer, QgsRectangle
from utils import data_path

qgis = QgsApplication([], False)
qgis.initQgis()

# raster layer
raster_layer = QgsRasterLayer(data_path("nahodny_raster.tif").as_posix(), "náhodný raster", "gdal")

# info o rasteru
print(raster_layer.crs())
print(raster_layer.extent())
print(raster_layer.isValid())

print(f"Raster size: {raster_layer.width()} - {raster_layer.height()}")
print(f"Bands: {raster_layer.bandCount()}")
print(f"Band 1 name:  {raster_layer.bandName(1)}")

# data provider
raster_layer_dp = raster_layer.dataProvider()

# extent pro blok dat
layer_extent = raster_layer.extent()
extent = QgsRectangle(
    layer_extent.xMinimum() + 10_000,
    layer_extent.yMinimum() + 10_000,
    layer_extent.xMaximum() - 10_000,
    layer_extent.yMaximum() - 10_000,
)

# extrakce bloku dat - může být rozsáhlý
block = raster_layer_dp.block(1, extent, 10, 10)

# blok = kompletní data
# raster_layer_dp.block(1, raster_layer.extent(), raster_layer.width(), raster_layer.height())

# iterace přes hodnoty bloku
for i in range(block.width()):
    for j in range(block.height()):
        print(f"{i} - {j} : {block.value(j, i)} ({block.isNoData(j, i)})")


# iterátor přes rastr
raster_iterator = QgsRasterIterator(raster_layer_dp)

# rozměr tilu rastru a nastavení na maximálně 100 x 100
print(f"Default Tile size = {raster_iterator.maximumTileHeight()} - {raster_iterator.maximumTileWidth()}")
raster_iterator.setMaximumTileHeight(100)
raster_iterator.setMaximumTileWidth(100)

# nastavení čtení rastru - čteme kompletní rozsah rastru a jeho skutečný rozsah počtu sloupců a řádků
raster_iterator.startRasterRead(1, raster_layer.width(), raster_layer.height(), raster_layer.extent())

# načtení aktuálního bloku dat a jeho informace (korektnost bloku, počet sloupců a řádků, blok, levý horní roh)
returned, columns, rows, block, top_left_x, top_left_y = raster_iterator.readNextRasterPart(1)

count = 0
while returned:
    print(f"{count} - {block.width()} : {block.height()}")
    count += 1
    # další blok dat pro cyklus
    returned, columns, rows, block, top_left_x, top_left_y = raster_iterator.readNextRasterPart(1)
