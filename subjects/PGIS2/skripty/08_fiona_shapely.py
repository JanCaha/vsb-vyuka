# NOTE: Ukázka práce s Fiona a Shapely: čtení vektorových dat, transformace CRS, buffer a zápis do GPKG
import fiona
import pyproj
from shapely.geometry import MultiPolygon, mapping, shape
from shapely.ops import transform
from utils import data_path, save_data_path

if __name__ == "__main__":

    path_data = data_path("ne_10m_admin_0_countries.shp")
    path_result_file = save_data_path("data.gpkg", delete_if_exist=True)

    # context manager pro čtení dat
    with fiona.open(path_data) as src:

        # schéma dat
        result_schema = src.schema.copy()
        # přidání a modifikace atributů
        result_schema["properties"]["area"] = "float"
        result_schema["geometry"] = "MultiPolygon"

        # souřadnicové systémy a konverzní objekt mezi nimi
        crs_src = pyproj.CRS(src.crs)
        crs_dst = pyproj.CRS("EPSG:3857")
        transformer = pyproj.Transformer.from_crs(crs_src, crs_dst, always_xy=True)

        # kontext manager pro tvorbu dat
        with fiona.open(
            path_result_file,
            mode="w",
            layer="countries",
            crs=crs_dst,
            driver="GPKG",
            schema=result_schema,
        ) as dst:

            feature: fiona.Feature
            for feature in src:

                # Shapely geometrie
                geom = shape(feature.geometry)

                # konverze do jiného CRS
                geom_transformed = transform(transformer.transform, geom)

                # buffer geometrie
                geom_transformed = geom_transformed.buffer(10_000)

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
