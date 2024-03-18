CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;

-- upgrade from previous versions
--SELECT postgis_extensions_upgrade();

-- routing functionality
-- CREATE EXTENSION pgrouting;

SELECT PostGIS_Full_Version();