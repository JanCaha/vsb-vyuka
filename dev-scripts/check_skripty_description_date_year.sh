#!/bin/bash

set -euo pipefail

BASE_DIR=$(dirname "$(realpath "$0")")
BASE_DIR=$(realpath "$BASE_DIR/..")

cd "$BASE_DIR" || exit 1

CURRENT_YEAR=$(date +%Y)

if ! command -v yq >/dev/null 2>&1; then
    echo "ERROR: yq is required to run this hook" >&2
    exit 1
fi

if [[ "$#" -eq 0 ]]; then
    echo "ERROR: no skripty files were provided by pre-commit" >&2
    exit 1
fi

for file in "$@"; do
    if [[ ! -f "$file" ]]; then
        echo "ERROR: file not found: $file" >&2
        exit 1
    fi

    if [[ "$file" != subjects/*/skripty/* ]]; then
        echo "ERROR: unsupported path outside skripty: $file" >&2
        exit 1
    fi

    description_yaml="$(dirname "$file")/description.yaml"
    relative_path="${file#subjects/}"

    if [[ ! -f "$description_yaml" ]]; then
        echo "ERROR: missing sibling description.yaml for $file" >&2
        exit 1
    fi

    file_date="$(yq -r --arg target_path "$relative_path" '.[] | select(.path == $target_path or .path == ("subjects/" + $target_path)) | .date' "$description_yaml" | head -n 1)"

    if [[ -z "$file_date" ]]; then
        echo "ERROR: $description_yaml has no matching entry for $file" >&2
        exit 1
    fi

    if [[ "$file_date" =~ ^([0-9]{4}) ]]; then
        file_year=${BASH_REMATCH[1]}
    else
        echo "ERROR: $description_yaml has an unsupported date format for $file: $file_date" >&2
        exit 1
    fi

    if [[ "$file_year" != "$CURRENT_YEAR" ]]; then
        echo "ERROR: $file has date year $file_year in $description_yaml, expected $CURRENT_YEAR" >&2
        exit 1
    fi
done