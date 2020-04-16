#!/bin/sh -l
set -e

for manifestfile in $(find $GITHUB_WORKSPACE -type f -name manifest.json); do
    python3 -m script.hassfest --action validate --integration-path "$(dirname -- "$manifestfile")"
done