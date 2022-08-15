#!/bin/bash

set -e

# Create necessary folder
mkdir -p rawdata

# Get all nodes and edges information
echo -e $(nix-instantiate --eval --json --strict --show-trace default.nix -A info) >rawdata/nodes.json

# # Generate the first graph
nix-shell shell.nix --run "
    python3 -m venv .venv;
    source .venv/bin/activate;
    pip install -e .;
    python3 -m nixpkgs_graph;
"
