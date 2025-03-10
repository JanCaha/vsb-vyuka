import utils
from osgeo import gdal, ogr

gdal.UseExceptions()


def use_memory_driver() -> None:
    path_data = utils.data_path("ne_10m_admin_0_countries.shp")
    path_result_file = utils.save_data_path("data.gpkg")

    params = gdal.VectorTranslateOptions(format="Memory", dstSRS="EPSG:3857")

    # NOTE: pokud se hodnota této proměnné změní, pak už se nebude možné dostat k datům !!!
    ds: gdal.Dataset = gdal.VectorTranslate("", path_data, options=params)

    with utils.LayerFromDatasetContextManager(ds) as layer:

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

    path_data = utils.data_path("ne_10m_admin_0_countries.shp")
    path_result = utils.base_save_data_path()

    params = gdal.VectorTranslateOptions(dstSRS="EPSG:3857")

    # NOTE: k datům se lze po dobu běhu skriptu dostat pod uvedenou adresou
    ds: gdal.Dataset = gdal.VectorTranslate("/vsimem/data.gpkg", path_data, options=params)

    with utils.LayerFromDatasetContextManager(ds) as layer:

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
