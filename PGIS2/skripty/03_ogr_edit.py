from pathlib import Path

import utils
from osgeo import gdal, ogr

gdal.UseExceptions()


def use_memory_driver() -> None:
    path_data = utils.data_path("ne_10m_admin_0_countries.shp")
    path_result_file = Path(__file__).parent / "data.gpkg"

    params = gdal.VectorTranslateOptions(format="Memory", dstSRS="EPSG:3857")

    # NOTE: pokud se hodnota této proměnné změní, pak už se nebude možné dostat k datům !!!
    ds: gdal.Dataset = gdal.VectorTranslate("", path_data, options=params)

    layer: ogr.Layer = ds.GetLayer()

    feature: ogr.Feature

    for feature in layer:
        geom: ogr.Geometry = feature.GetGeometryRef()

        feature.SetGeometry(geom.Buffer(10 * 1000))

        layer.UpsertFeature(feature)

    layer = None

    gdal.VectorTranslate(path_result_file, ds)

    ds = None


def use_in_memory_data() -> None:

    path_data = utils.data_path("ne_10m_admin_0_countries.shp")
    path_result = Path(__file__).parent

    params = gdal.VectorTranslateOptions(dstSRS="EPSG:3857")

    # NOTE: k datům se lze po dobu běhu skriptu dostat pod uvedenou adresou
    ds: gdal.Dataset = gdal.VectorTranslate("/vsimem/data.gpkg", path_data, options=params)

    layer: ogr.Layer = ds.GetLayer()

    feature: ogr.Feature

    for feature in layer:
        geom: ogr.Geometry = feature.GetGeometryRef()

        feature.SetGeometry(geom.Buffer(10 * 1000))

        layer.UpsertFeature(feature)

    layer = None

    gdal.Sync(
        "/vsimem/",
        path_result,
    )

    ds = None


if __name__ == "__main__":

    use_in_memory_data()
