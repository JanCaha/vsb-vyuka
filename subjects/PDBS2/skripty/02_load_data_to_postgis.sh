PG_CONN="dbname=postgres host=localhost user=postgres port=5432 password=heslo"

# uložení vrstvy z GPKG do PostGIS
ogr2ogr -nln kraje "Pg:$PG_CONN" uzemni_jednotky.gpkg kraje
ogr2ogr -nln okresy "Pg:$PG_CONN" uzemni_jednotky.gpkg okresy

# uložení dat z PostGIS do souboru
ogr2ogr okresy.geojson "Pg:$PG_CONN" okresy
ogr2ogr okresy.gpkg "Pg:$PG_CONN" okresy
