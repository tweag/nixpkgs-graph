#!/bin/bash

set -e

# Get raw nodes information
mkdir -p rawdata
nix search --json nixpkgs >rawdata/nodes.json

# Convert nodes.json to csv format
./node_format_trans.py
