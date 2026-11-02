#!/bin/bash

# Script pro zabalení Python balíčků 

BASE_DIR=$(dirname "$(realpath "$0")")
BASE_DIR=$(realpath "$BASE_DIR/..")

echo "🔄 Přepnutí do základního adresáře: $BASE_DIR"

cd "$BASE_DIR" || exit 1

echo "📦 Balení Python balíčků..."
echo "=============================="

# PGIS2 balíček
echo "📦 Balení PGIS2 balíčku..."
FILE="$BASE_DIR/subjects/PGIS2/skripty/balik_pgis2.zip"
TMP_FILE="/tmp/balik_pgis2.zip"

cd $BASE_DIR/baliky
# smaž nepotřebné složky
find "balik_pgis2" -type d \( -name build  -o -name .pytest_cache -o -name __pycache__ -o -name "*.egg-info" \) -exec rm -rf {} + 2>/dev/null

zip -r "$TMP_FILE" "balik_pgis2"
rsync -c "$TMP_FILE" "$FILE"

echo "✓ PGIS2 balíček sbalen: $FILE"
echo "=============================="

# PGIS3 balíček
echo "📦 Balení PGIS3 balíčku..."
FILE="$BASE_DIR/subjects/PGIS3/skripty/balik_pgis3.zip"
TMP_FILE="/tmp/balik_pgis3.zip"

cd $BASE_DIR/baliky
# smaž nepotřebné složky
find "balik_pgis3" -type d \( -name build  -o -name .pytest_cache -o -name __pycache__ -o -name "*.egg-info" \) -exec rm -rf {} + 2>/dev/null

zip -r "$TMP_FILE" "balik_pgis3"
rsync -c "$TMP_FILE" "$FILE"
echo "✓ PGIS3 balíček sbalen: $FILE"
echo "=============================="

echo ""
echo "✅ Balení dokončeno!"