SCRIPT_DIR=$(dirname "$0")

DATA_DIR=$SCRIPT_DIR/../_data

getData () {
    if [ ! -f "$DATA_DIR/$1" ]; then
        wget -P $DATA_DIR "$2/$1"
    fi
    unzip -o -d $DATA_DIR "$DATA_DIR/$1"
}

FILE=ne_10m_admin_0_countries.zip
SOURCE_URL=https://naciscdn.org/naturalearth/10m/cultural
getData $FILE $SOURCE_URL

FILE=HYP_HR_SR_W.zip
SOURCE_URL=https://naciscdn.org/naturalearth/10m/raster
getData $FILE $SOURCE_URL
