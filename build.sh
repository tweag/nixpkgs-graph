#!/bin/bash

set -e

# Generate and analyze the graph
nix-shell shell.nix --run "
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -e .
    python3 -m nixpkgs_graph build --rev ${1:-481f9b246d200205d8bafab48f3bd1aeb62d775b} --sha256 ${2:-0n6a4a439md42dqzzbk49rfxfrf3lx3438i2w262pnwbi3dws72g} --output ./rawdata/nodes.json
    python3 -m nixpkgs_graph generate-graph --input-file ./rawdata/nodes.json --output-folder ./rawdata/
    
    cp ./rawdata/start.graphml \$NEO4J_HOME/share/neo4j/import/
    cypher-shell -a bolt://localhost:7687 \"call apoc.import.graphml('start.graphml', {})\"
    cypher-shell -a bolt://localhost:7687 \"match (n) detach delete n\"

    cp ./rawdata/first_graph.graphml \$NEO4J_HOME/share/neo4j/import/
    cypher-shell -a bolt://localhost:7687 \"call apoc.import.graphml('first_graph.graphml', {})\"
"
