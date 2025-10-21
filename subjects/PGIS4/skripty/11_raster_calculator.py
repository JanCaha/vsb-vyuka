import utils
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.core import QgsApplication, QgsProject, QgsRasterFileWriter, QgsRasterLayer

qgis = QgsApplication([], False)
qgis.initQgis()

raster_layer = QgsRasterLayer(utils.data_path("nahodny_raster.tif").as_posix(), "rasterova_vrstva", "gdal")

# záznam pro RasterCalculator
# ref se bude používat ve výrazu kalkulátoru a musí být unikátní, tady je vyrábíme z názvu vrstvy, ale může být zcela libovolné
# zbytek jsou vlastnosti
r_calc_1 = QgsRasterCalculatorEntry()
r_calc_1.ref = f"{raster_layer.name()}@1"  # ale může být třeba: "a@1" a i část s "@1" je spíše konvence označující pásmo, než nezbytnost
r_calc_1.raster = raster_layer
r_calc_1.bandNumber = 1

# seznam záznamu pro RasterCalculator
rasters_entries_for_calculator = [r_calc_1]

# výraz pro výpočet - stejný jako sestavíme v GUI QGIS např.
# dopručuju vyzkoušet v GUI QGIS a pak zkopírovat - alespoň pro začátek
raster_calculator_expression = f"{r_calc_1.ref} * 5 - 25"
# výrazy podporují i funkce, např.: "if ( ("vypocet_rastru@1" * 10) >= 250, 1, 0 )""

# název výstupního souboru
output_file = utils.save_data_path("vypocet_rastru.tif")


raster_calulator = QgsRasterCalculator(
    raster_calculator_expression,
    output_file.as_posix(),
    QgsRasterFileWriter.driverForExtension(output_file.suffix),
    raster_layer.extent(),
    raster_layer.crs(),
    raster_layer.width(),
    raster_layer.height(),
    rasters_entries_for_calculator,
    QgsProject.instance().transformContext(),
)

# spuštění výpočtu
raster_calulator.processCalculation()

# získáme chybu, pokud nějaká nastala
error = raster_calulator.lastError()

if error:
    print(f"Chyba výpočtu rastru: {error}")
else:
    print(f"Výpočet rastru dokončen, výstupní soubor: {output_file.as_posix()}")
