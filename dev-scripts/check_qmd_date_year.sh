#!/bin/bash

set -euo pipefail

BASE_DIR=$(dirname "$(realpath "$0")")
BASE_DIR=$(realpath "$BASE_DIR/..")

cd "$BASE_DIR" || exit 1

CURRENT_YEAR=$(date +%Y)
FAILED=0

if [[ "$#" -eq 0 ]]; then
    echo "ERROR: no files were provided by pre-commit" >&2
    exit 1
fi

for file in "$@"; do
    in_front_matter=0
    has_date=0
    date_year=""

    while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ "$line" == "---" && "$in_front_matter" -eq 0 ]]; then
            in_front_matter=1
            continue
        fi

        if [[ "$in_front_matter" -eq 1 && "$line" == "---" ]]; then
            break
        fi

        if [[ "$in_front_matter" -eq 1 && "$line" =~ ^[[:space:]]*date:[[:space:]]*(.+)$ ]]; then
            has_date=1
            if [[ ${BASH_REMATCH[1]} =~ ([0-9]{4}) ]]; then
                date_year=${BASH_REMATCH[1]}
            fi
            break
        fi
    done < "$file"

    if [[ "$has_date" -eq 1 && "$date_year" != "$CURRENT_YEAR" ]]; then
        echo "ERROR: $file has date year $date_year, expected $CURRENT_YEAR" >&2
        FAILED=1
    fi
done

exit "$FAILED"