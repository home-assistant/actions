#!/bin/bash
set -e

declare -a INTEGRATIONS

for manifestfile in $(find $GITHUB_WORKSPACE -type f -name manifest.json); do
    INTEGRATIONS+=(--integration-path)
    INTEGRATIONS+=("$(dirname -- ${manifestfile})")
done

if [ "${INTEGRATIONS}" = "" ]; then
    echo "No integrations found!"
    exit 1
fi
echo "${INTEGRATIONS[@]}"
python3 -m script.hassfest --action validate "${INTEGRATIONS[@]}"