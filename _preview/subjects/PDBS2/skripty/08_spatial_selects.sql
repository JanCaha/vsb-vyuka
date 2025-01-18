-- contains
WITH kraj_polygon AS (
    SELECT geom FROM kraje WHERE nazev = 'Moravskoslezský kraj'
)
SELECT nazev FROM okresy, kraj_polygon WHERE ST_Contains( kraj_polygon.geom, okresy.geom);

-- contains properly
WITH kraj_polygon AS (
    SELECT geom FROM kraje WHERE nazev = 'Moravskoslezský kraj'
)
SELECT nazev FROM okresy, kraj_polygon WHERE ST_ContainsProperly( kraj_polygon.geom, okresy.geom);

-- intersercts
WITH kraj_polygon AS (
    SELECT geom FROM kraje WHERE nazev = 'Moravskoslezský kraj'
)
SELECT nazev FROM okresy, kraj_polygon WHERE ST_Intersects( kraj_polygon.geom, okresy.geom);

-- touches
WITH kraj_polygon AS (
    SELECT geom FROM kraje WHERE nazev = 'Moravskoslezský kraj'
)
SELECT nazev FROM okresy, kraj_polygon WHERE ST_Touches( kraj_polygon.geom, okresy.geom);

-- identify
SELECT nazev FROM okresy WHERE ST_Intersects(okresy.geom,  ST_Transform(ST_SetSRID(ST_Point(18.01, 49.88),4326), 5514))

