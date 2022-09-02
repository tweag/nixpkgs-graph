#!/bin/bash

set -e

# Generate and analyze the graph
nix-shell shell.nix --run "
    python -m venv .venv
    source .venv/bin/activate
    pip install -e .
    python -m nixpkgs_graph build --rev $1 --sha256 $2 --output ./rawdata/nodes.json
    python -m nixpkgs_graph generate-graph --input-file ./rawdata/nodes.json --output-folder ./rawdata/
    echo \"apoc.import.file.enabled=true\" >> $NEO4J_HOME/share/neo4j/conf/neo4j.conf
    echo \"dbms.security.auth_enabled=false\" >> $NEO4J_HOME/share/neo4j/conf/neo4j.conf
    cp ./rawdata/first_graph.graphml \$NEO4J_HOME/share/neo4j/import/
    cypher-shell -a bolt://localhost:7687 \"call apoc.import.graphml('first_graph.graphml', {})\"
"
