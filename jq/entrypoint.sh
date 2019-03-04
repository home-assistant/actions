#!/bin/bash
set -e
shopt -s globstar

cat -- $* | jq '.'
