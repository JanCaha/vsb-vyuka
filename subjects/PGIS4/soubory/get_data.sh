SCRIPT_DIR=$(dirname "$0")

DATA_DIR=$SCRIPT_DIR/../_data

mkdir -p $DATA_DIR

cp $CONDA_PREFIX/share/qgis/resources/data/world_map.gpkg $DATA_DIR/world.gpkg

qgis_process run native:createrandomuniformrasterlayer \
    --distance_units=meters --area_units=m2 --ellipsoid=EPSG:7030 \
    --EXTENT='1329618.912500000,2120366.292900000,6193438.152600000,6642251.185800000 [EPSG:3857]' --TARGET_CRS='EPSG:5514' \
    --PIXEL_SIZE=100 --OUTPUT_TYPE=5 --LOWER_BOUND=0 --UPPER_BOUND=100 \
    --OUTPUT=$DATA_DIR/nahodny_raster.tif

cp $DATA_DIR/nahodny_raster.tif $DATA_DIR/nahodny_raster_upravy.tif
cp $SCRIPT_DIR/projekt1.qgz $DATA_DIR/projekt1.qgz