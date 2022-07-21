#!/bin/bash

set -e

# Create necessary folder
mkdir -p rawdata
export NIXPKGS_ALLOW_UNFREE=1
# Get all nodes and edges information
echo -e $(nix-instantiate --eval --json --strict --keep-going default.nix -A info) >rawdata/edges.json
