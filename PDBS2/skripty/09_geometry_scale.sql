CREATE VIEW okresy_scaled AS (
	WITH okresy_ratio AS (
		WITH okresy_rozloha AS (
			SELECT ST_AREA(geom) as rozloha, nazev, geom FROM okresy
		),
		max_rozloha AS(
			SELECT max(rozloha) AS value FROM okresy_rozloha
		)
		SELECT nazev, rozloha, rozloha/max_rozloha.value as ratio, geom, ST_Centroid(geom) as centroid FROM okresy_rozloha, max_rozloha
	)
	SELECT rozloha, ratio, nazev, ST_Translate(ST_Scale(ST_Translate(geom, -ST_X(centroid),-ST_Y(centroid)), ratio, ratio), ST_X(centroid), ST_Y(centroid)) as geom FROM okresy_ratio
)
