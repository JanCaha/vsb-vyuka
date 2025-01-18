CREATE VIEW okresy_obyvatele_2020 AS (
    WITH obyvatele_kraje_2020 AS(
        SELECT 
            hodnota AS pocet_obyvatel,
            kod_ruian::TEXT
        FROM obyvatele_roky
        LEFT OUTER JOIN ciselnik_csu_ruian ON (uzemi_kod = kod_csu)
        WHERE obdobi LIKE '2020-%'
    )
    SELECT nazev, kod_ruian, lau1_kod, ST_Transform(geom, 4326)::geometry(Geometry, 4326) As geom, pocet_obyvatel
    FROM okresy
    LEFT OUTER JOIN obyvatele_kraje_2020 ON (kod = kod_ruian)
)