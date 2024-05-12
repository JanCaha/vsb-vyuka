CREATE EXTENSION  IF NOT EXISTS postgis;
CREATE EXTENSION  IF NOT EXISTS postgis_topology;

-- upgrade from previous versions
--SELECT postgis_extensions_upgrade();

-- routing functionality
-- CREATE EXTENSION pgrouting;

SELECT PostGIS_Full_Version();