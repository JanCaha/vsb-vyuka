# NOTE: Načtení vektorových dat, získání vrstvy a základní informací o vrstvě,
# nastavení prostorového filtru a výpis prvků vyhovujících tomuto pravidlu
from osgeo import gdal, ogr, osr
from utils import LayerContextManager, data_path

# způsobí že chyby v GDAL budou vyvolávat výjimky
gdal.UseExceptions()


def create_box(min_x: float, max_x: float, min_y: float, max_y: float) -> ogr.Geometry:
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(min_x, min_y)
    ring.AddPoint(max_x, min_y)
    ring.AddPoint(max_x, max_y)
    ring.AddPoint(min_x, max_y)
    ring.AddPoint(min_x, min_y)

    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(ring)

    return polygon


if __name__ == "__main__":
    file = data_path("ne_10m_admin_0_countries.shp")

    print(file.exists())

    ds: gdal.Dataset = gdal.OpenEx(file.as_posix())

    layer: ogr.Layer = ds.GetLayer()

    srs: osr.SpatialReference = layer.GetSpatialRef()

    print(layer.GetName())
    print(layer.GetFeatureCount())
    print(f"{srs.GetAuthorityName(None)}:{srs.GetAuthorityCode(None)}")
    print("-" * 10)

    # NOTE: All features in layer
    # feature: ogr.Feature
    # for feature in layer:
    #     print(feature.GetField("SOVEREIGNT"))

    layer.SetSpatialFilter(create_box(0, 20, 35, 50))

    print(layer.GetFeatureCount())

    feature: ogr.Feature

    for feature in layer:
        geom: ogr.Geometry = feature.geometry()
        name = feature.GetField("Name")
        print(f"{name} - {geom.Area()}")
