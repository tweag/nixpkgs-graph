#!/bin/bash

set -e

# Create necessary folder
mkdir -p rawdata

export NIXPKGS_ALLOW_INSECURE=1
export NIXPKGS_ALLOW_UNFREE=1
export NIXPKGS_ALLOW_UNSUPPORTED_SYSTEM=1
# Get all nodes and edges information
echo -e $(nix-instantiate --eval --json --strict --keep-going default.nix -A info1) >rawdata/edges.json
# echo -e $(nix-instantiate --eval default.nix -A info1) >rawdata/edges.json
