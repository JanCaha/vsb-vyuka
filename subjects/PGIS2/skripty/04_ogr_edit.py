# NOTE: Ukázka uložení dat do paměti (s formátem i bez formátu) a modifikace dat v paměti
from osgeo import gdal, ogr
from utils import LayerFromDatasetContextManager, base_save_data_path, data_path, save_data_path

gdal.UseExceptions()


def use_memory_driver() -> None:
    """Použití bezformátového memory driveru pro načtení dat do paměti, modifikaci a uložení do souboru"""

    path_data = data_path("ne_10m_admin_0_countries.shp")
    path_result_file = save_data_path("data.geojson")

    params = gdal.VectorTranslateOptions(format="MEM", dstSRS="EPSG:3857")

    # NOTE: pokud se hodnota této proměnné změní, pak už se nebude možné dostat k datům !!!
    ds: gdal.Dataset = gdal.VectorTranslate("", path_data, options=params)

    with LayerFromDatasetContextManager(ds) as layer:

        feature: ogr.Feature

        for feature in layer:

            # úprava geometrie prvku
            geom: ogr.Geometry = feature.GetGeometryRef()
            feature.SetGeometry(geom.Buffer(10 * 1000))

            # funkce pro nahrazení či vytvoření (pokud neexistuje - identifikace přes FID) prvku
            layer.UpsertFeature(feature)

    gdal.VectorTranslate(path_result_file, ds)

    ds = None


def use_in_memory_data() -> None:
    """Použití dat v paměti ve formátu GPKG, modifikace a synchronizace s cílovou složkou"""

    path_data = data_path("ne_10m_admin_0_countries.shp")
    path_result = base_save_data_path()

    params = gdal.VectorTranslateOptions(dstSRS="EPSG:3857")

    # NOTE: k datům se lze po dobu běhu skriptu dostat pod uvedenou adresou
    ds: gdal.Dataset = gdal.VectorTranslate("/vsimem/data.gpkg", path_data, options=params)

    with LayerFromDatasetContextManager(ds) as layer:

        feature: ogr.Feature

        for feature in layer:

            # úprava geometrie prvku
            geom: ogr.Geometry = feature.GetGeometryRef()
            feature.SetGeometry(geom.Buffer(10 * 1000))

            # funkce pro nahrazení či vytvoření (pokud neexistuje - identifikace přes FID) prvku
            layer.UpsertFeature(feature)

    # funkce sychronizuje obsah dvou složek, první je zdrojová lokace, druhá je cílová lokace
    # první parametr může i odkazovat do /vsimem prostoru
    gdal.Sync(
        "/vsimem/",
        path_result,
    )

    ds = None


if __name__ == "__main__":

    # použití memory driveru
    use_memory_driver()

    # použití in-memory dat
    use_in_memory_data()
