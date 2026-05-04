# NOTE: Ukázka nástroje VectorTranslate pro konverzi a úpravy dat, použití paměti pro uložení dat
from osgeo import gdal, ogr
from utils import data_path, save_data_path

gdal.UseExceptions()

if __name__ == "__main__":
    file = data_path("ne_10m_admin_0_countries.shp")

    print(f"Soubor existuje: {file.exists()}")

    ds: gdal.Dataset = gdal.OpenEx(file)

    options = gdal.VectorTranslateOptions(
        format="MEM",  # memory formát bez specifického typu uložení, existuje pouze v RAM
        dstSRS="EPSG:3857",  # výstupní souřadnicový systém - konverze
        layerName="ne_10m_admin_0_countries",  # název vrstvy - není povinný, pokud existuje pouze jedna vrstva nebo chceme-li všechny
        spatFilter=(0, 35, 20, 50),  # min_x, min_y, max_x, max_y - velice přibližně střední Evropa
        geometryType=["PROMOTE_TO_MULTI"],  # převedení geometrie na multi geometrii - zabrání výpisu varování
    )

    ds_extracted: gdal.Dataset = gdal.VectorTranslate("", ds, options=options)

    layer_extracted: ogr.Layer = ds_extracted.GetLayer()

    print(layer_extracted.GetFeatureCount())

    # operace s daty z vrstvy zde - např. modifikace hodnot

    layer_extracted = None  # explicitní uvolnění vrstvy

    output_file_path = save_data_path("extracted.gpkg", delete_if_exist=True)

    # v posledních verzích GDAL podporuje i cesty typu pathlib.Path, ve starších verzích by bylo nutné cestu zadat jako `soubor_vysledny.as_posix()`
    gdal.VectorTranslate(output_file_path, ds_extracted)

    print(f"Dokončeno, soubor existuje: {output_file_path.exists()}")
