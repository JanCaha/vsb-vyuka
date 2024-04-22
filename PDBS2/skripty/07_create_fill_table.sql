DROP TABLE IF EXIST kraje_obyvatele;
CREATE TABLE kraje_obyvatele;(
    id SERIAL PRIMARY KEY,
    pocet_obyvatel integer,
    nazev TEXT,
    geom Geometry(MULTIPOLYGON, 5514)
);

WITH obyvatele_kraje_2020 AS (
    WITH obyvatele_2020 AS(
        SELECT 
            hodnota AS pocet_obyvatel,
            kod_ruian::TEXT
        FROM obyvatele_roky
        LEFT OUTER JOIN ciselnik_csu_ruian ON (uzemi_kod = kod_csu)
        WHERE obdobi LIKE '2020-%'
    )
    SELECT pocet_obyvatel, nazev, ST_Transform(geom, 5514)::geometry(Geometry, 5514) As geom FROM kraje
    LEFT OUTER JOIN obyvatele_2020 ON (kod = kod_ruian)
)
INSERT INTO kraje_obyvatele(pocet_obyvatel, nazev, geom) 
SELECT * FROM obyvatele_kraje_2020;