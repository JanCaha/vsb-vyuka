from pathlib import Path

import fiona
import pyproj
import utils
from shapely.geometry import MultiPolygon, mapping, shape
from shapely.ops import transform

if __name__ == "__main__":

    path_data = utils.data_path("ne_10m_admin_0_countries.shp")
    path_result_file = Path(__file__).parent / "data.gpkg"

    with fiona.open(path_data) as src:

        result_schema = src.schema
        result_schema["properties"]["area"] = "float"
        result_schema["geometry"] = "MultiPolygon"

        crs_src = pyproj.CRS(src.crs)
        crs_dst = pyproj.CRS("EPSG:3857")

        project = pyproj.Transformer.from_crs(crs_src, crs_dst, always_xy=True).transform

        with fiona.open(
            path_result_file,
            mode="w",
            layer="countries",
            crs=src.crs,
            driver="GPKG",
            schema=result_schema,
        ) as dst:

            feat: fiona.Feature

            i = 0
            for feat in src:

                geom = shape(feat.geometry)
                geom_transformed = transform(project, geom)
                geom_transformed = geom_transformed.buffer(10 * 1000)

                if geom_transformed.geom_type != "MultiPolygon":
                    geom_transformed = MultiPolygon([geom_transformed])

                new_geom = fiona.Geometry.from_dict(mapping(geom_transformed))
                props = fiona.Properties.from_dict(**feat.properties, area=geom_transformed.area)

                new_feat = fiona.Feature(geometry=new_geom, properties=props)
                dst.write(new_feat)
