#!/bin/bash

set -e

# Create necessary folder
mkdir -p rawdata

# Get all nodes and edges information
echo -e $(nix-instantiate --eval default.nix -A file) >rawdata/edges.txt
