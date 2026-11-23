from pathlib import Path

import processing
from qgis.core import (
    Qgis,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
    QgsRasterBlock,
    QgsRasterFileWriter,
    QgsRasterIterator,
)


class RasterThresholdClassificationAlgorithm(QgsProcessingAlgorithm):
    INPUT = "vstupni_vrstva"
    OUTPUT = "vystupni_vrstva"
    NUMERICALLIMIT = "ciselny_limit"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT,
                "Vstupní vrstva",
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.NUMERICALLIMIT,
                "Limitní hodnota",
                QgsProcessingParameterNumber.Type.Double,
                defaultValue=1000,
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT,
                "Výsledná vrstva",
            )
        )

    def processAlgorithm(self, parameters, context, model_feedback):
        vstupni_raster = self.parameterAsRasterLayer(
            parameters,
            self.INPUT,
            context,
        )

        if vstupni_raster is None:
            raise QgsProcessingException(self.invalidRasterError(parameters, self.INPUT))

        ciselny_limit = self.parameterAsDouble(
            parameters,
            self.NUMERICALLIMIT,
            context,
        )

        vystupni_raster_umisteni = self.parameterAsOutputLayer(
            parameters,
            self.OUTPUT,
            context,
        )

        raster_writer = QgsRasterFileWriter(vystupni_raster_umisteni)

        raster_writer.setOutputProviderKey("gdal")

        ext = Path(vystupni_raster_umisteni).suffix.replace(".", "")

        driver = raster_writer.driverForExtension(ext)

        raster_writer.setOutputFormat(driver)

        vysledny_raster_dataprovider = raster_writer.createOneBandRaster(
            Qgis.Float32,
            vstupni_raster.width(),
            vstupni_raster.height(),
            vstupni_raster.extent(),
            vstupni_raster.crs(),
        )

        if not vysledny_raster_dataprovider:
            raise QgsProcessingException("Nelze vytvořit výsledný raster.")

        vysledny_raster_dataprovider.setNoDataValue(1, vstupni_raster.dataProvider().sourceNoDataValue(1))

        raster_iter = QgsRasterIterator(vstupni_raster.dataProvider())

        raster_iter.startRasterRead(
            1,
            vstupni_raster.dataProvider().xSize(),
            vstupni_raster.dataProvider().ySize(),
            vstupni_raster.extent(),
        )

        raster_iter.setMaximumTileHeight(1)
        raster_iter.setMaximumTileWidth(1)

        (
            correct,
            n_cols,
            n_rows,
            data_block,
            top_left_col,
            top_left_row,
        ) = raster_iter.readNextRasterPart(1)

        new_block = QgsRasterBlock(Qgis.Float32, n_cols, n_rows)
        new_block.setNoDataValue(vstupni_raster.dataProvider().sourceNoDataValue(1))

        while correct:
            for i in range(data_block.width() * data_block.height()):
                value = 0
                if data_block.value(i) > ciselny_limit:
                    value = 1
                new_block.setValue(i, value)

            vysledny_raster_dataprovider.writeBlock(
                new_block,
                1,
                top_left_col,
                top_left_row,
            )

            (
                correct,
                n_cols,
                n_rows,
                data_block,
                top_left_col,
                top_left_row,
            ) = raster_iter.readNextRasterPart(1)

            if correct:
                new_block = QgsRasterBlock(Qgis.Float32, n_cols, n_rows)
                new_block.setNoDataValue(vstupni_raster.dataProvider().sourceNoDataValue(1))

        return {self.OUTPUT: vystupni_raster_umisteni}

    def name(self):
        return "raster_threshold_classification"

    def displayName(self):
        return "Kategorizace rastru dle limitu"

    def group(self):
        return "PGIS4 - Rastrové nástroje"

    def groupId(self):
        return "pgis4_raster_tools"

    def createInstance(self):
        return RasterThresholdClassificationAlgorithm()
