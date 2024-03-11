from pathlib import Path

from osgeo import gdal, ogr

gdal.UseExceptions()

file = Path(__file__).parent.parent.parent / "_data" / "ne_10m_admin_0_countries.shp"

print(file.exists())

ds: gdal.Dataset = gdal.OpenEx(file.as_posix())

layer: ogr.Layer = ds.GetLayer()

print(layer.GetName())
print(layer.GetFeatureCount())
