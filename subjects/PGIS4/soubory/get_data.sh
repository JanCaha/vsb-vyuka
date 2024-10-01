SCRIPT_DIR=$(dirname "$0")

DATA_DIR=$SCRIPT_DIR/../_data

mkdir -p $DATA_DIR

cp $CONDA_PREFIX/share/qgis/resources/data/world_map.gpkg $DATA_DIR/world.gpkg