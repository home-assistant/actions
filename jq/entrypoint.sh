#!/bin/bash
set -e
shopt -s globstar

jq $*
