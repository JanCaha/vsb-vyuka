#!/bin/bash

BASE_DIR=$(dirname "$(realpath "$0")")

# python balíček pro PGIS2 
cd dev
zip -r "../subjects/PGIS2/skripty/python_balicek.zip" "balicekpgis2"
cd balicekpgis2
pip install .
cd $BASE_DIR