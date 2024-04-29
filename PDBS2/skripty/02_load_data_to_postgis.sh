# uložení vrstvy z GPKG do PostGIS
ogr2ogr -nln kraje Pg:"dbname=postgres host=localhost user=postgres port=5432 password=heslo" uzemni_jednotky.gpkg kraje
ogr2ogr -nln okresy Pg:"dbname=postgres host=localhost user=postgres port=5432 password=heslo" uzemni_jednotky.gpkg okresy

# uložení dat z PostGIS do souboru
ogr2ogr okresy.geojson Pg:"dbname=postgres host=localhost user=postgres port=5432 password=heslo" okresy
ogr2ogr okresy.gpkg Pg:"dbname=postgres host=localhost user=postgres port=5432 password=heslo" okresy
