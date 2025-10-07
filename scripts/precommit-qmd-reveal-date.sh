#!/bin/bash

REQUIRED_LINE="date: "$(date +%Y-%m-%d)

# Najdi všechny změněné nebo přidané .qmd soubory
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.qmd$')

EXIT_CODE=0

for file in $FILES; do
    if grep -Fxq "revealjs:" "$file"; then
        if ! grep -Fxq "$REQUIRED_LINE" "$file"; then
            echo "ERROR: Soubor '$file' má nesprávné datum úpravy!"
            EXIT_CODE=1
        fi
    fi
done

exit $EXIT_CODE