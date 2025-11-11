#!/bin/bash

BASE_DIR=$(dirname "$(realpath "$0")")

# python balíček pro PGIS2 
cd dev
zip -r "../subjects/PGIS2/skripty/python_balicek.zip" "balicekpgis2"
cd balicekpgis2
pip install .
cd $BASE_DIR

# python balíček pro PGIS3 
cd dev
zip -r "../subjects/PGIS3/skripty/balik_pgis3.zip" "balik_pgis3"
cd balik_pgis3
pip install .
cd $BASE_DIR