PG_CON=Pg:"dbname=postgres host=localhost user=postgres port=5432 password=heslo"

ogr2ogr -nln kraje $PG_CON uzemni_jednotky.gpkg kraje
ogr2ogr -nln okresy $PG_CON uzemni_jednotky.gpkg okresy