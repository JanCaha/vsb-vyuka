from pathlib import Path

import fiona
import pyproj
import utils
from shapely.geometry import MultiPolygon, mapping, shape
from shapely.ops import transform

if __name__ == "__main__":
    import sys

    sys.exit(100)

    path_data = utils.data_path("ne_10m_admin_0_countries.shp")
    path_result_file = Path(__file__).parent / "data.gpkg"

    # context manager pro čtení dat
    with fiona.open(path_data) as src:

        # schéma dat
        result_schema = src.schema
        # přidání a modifikace atributů
        result_schema["properties"]["area"] = "float"
        result_schema["geometry"] = "MultiPolygon"

        # souřadnicové systémy a konverzní objekt mezi nimi
        crs_src = pyproj.CRS(src.crs)
        crs_dst = pyproj.CRS("EPSG:3857")
        project = pyproj.Transformer.from_crs(crs_src, crs_dst, always_xy=True).transform

        # kontext manager pro tvorbu dat
        with fiona.open(
            path_result_file,
            mode="w",
            layer="countries",
            crs=src.crs,
            driver="GPKG",
            schema=result_schema,
        ) as dst:

            feature: fiona.Feature

            i = 0
            for feature in src:

                # Shapely geometry
                geom = shape(feature.geometry)
                # konverze do jiného CRS
                geom_transformed = transform(project, geom)
                # buffer geometrie
                geom_transformed = geom_transformed.buffer(10 * 1000)

                if geom_transformed.geom_type != "MultiPolygon":
                    geom_transformed = MultiPolygon([geom_transformed])

                # konverze geometrie nazpět do geometrie Fiona
                new_geom = fiona.Geometry.from_dict(mapping(geom_transformed))
                # příprava atributů
                props = fiona.Properties.from_dict(**feature.properties, area=geom_transformed.area)

                # nový prvek
                new_feat = fiona.Feature(geometry=new_geom, properties=props)
                # zápis prvku
                dst.write(new_feat)
