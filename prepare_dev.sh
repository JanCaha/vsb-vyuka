#!/bin/bash

BASE_DIR=$(dirname "$(realpath "$0")")

# python balíček pro PGIS2 
cd dev
FILE="../subjects/PGIS2/skripty/python_balicek.zip"
rm
zip -r $FILE "balicekpgis2"
cd balicekpgis2
pip install .
cd $BASE_DIR

# python balíček pro PGIS3 
cd dev
FILE="../subjects/PGIS3/skripty/balik_pgis3.zip"
zip -r $FILE "balik_pgis3"
cd balik_pgis3
pip install .
cd $BASE_DIR