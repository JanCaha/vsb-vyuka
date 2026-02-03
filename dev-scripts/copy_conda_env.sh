#!/bin/bash
# Tento skript zkopíruje soubor conda-environment.yml do složky subjects/PGIS2/soubory
# Spouští se jako pre-commit/pre-push hook přes pre-commit framework

set -e

SRC="conda-environment.yml"
DEST="subjects/PGIS2/soubory/conda-environment.yml"

if [ -f "$SRC" ]; then
    cp "$SRC" "$DEST"
    echo "Copied $SRC to $DEST"
else
    echo "$SRC does not exist!"
    exit 1
fi
