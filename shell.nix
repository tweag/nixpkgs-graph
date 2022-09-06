{ pkgs ? import <nixpkgs> { }, pkgs1 ?
  import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/master.tar.gz")
  { }, rev ? "481f9b246d200205d8bafab48f3bd1aeb62d775b"
, sha256 ? "0n6a4a439md42dqzzbk49rfxfrf3lx3438i2w262pnwbi3dws72g" }:
let
  my-python = pkgs.python3;
  my-pip = pkgs.python3Packages.pip;
  pythonEnv = my-python.withPackages (p:
    with p; [
      matplotlib
      networkx
      pandas
      scipy
      click
      setuptools
      # other python packages needed here
    ]);
  neo4j = pkgs1.neo4j;
in pkgs.mkShell {
  buildInputs = [
    pythonEnv
    my-pip
    neo4j
    # other dependencies needed here
  ];
  shellHook = ''
    # Path set
    PYTHONPATH=${pythonEnv}/${pythonEnv.sitePackages}
    NEO4J_HOME=${neo4j}

    # Install Neo4j
    chmod 755 -R $NEO4J_HOME/share/neo4j/
    wget -P $NEO4J_HOME/share/neo4j/plugins/ -nc https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.4.0.1/apoc-4.4.0.1-all.jar
    neo4j start
    grep ^apoc.import.file.enabled=true $NEO4J_HOME/share/neo4j/conf/neo4j.conf || echo "apoc.import.file.enabled=true" >> $NEO4J_HOME/share/neo4j/conf/neo4j.conf
    grep ^dbms.security.auth_enabled=false $NEO4J_HOME/share/neo4j/conf/neo4j.conf || echo "dbms.security.auth_enabled=false" >> $NEO4J_HOME/share/neo4j/conf/neo4j.conf

    # Lance Python
    python -m venv .venv
    source .venv/bin/activate
    pip install -e .
    python -m nixpkgs_graph build --rev ${rev} --sha256 ${sha256} --output ./rawdata/nodes.json
    python -m nixpkgs_graph generate-graph --input-file ./rawdata/nodes.json --output-folder ./rawdata/

    # Log data to Neo4j
    cp ./rawdata/start.graphml $NEO4J_HOME/share/neo4j/import/
    cp ./rawdata/first_graph.graphml $NEO4J_HOME/share/neo4j/import/
    cypher-shell -a bolt://localhost:7687 "call apoc.import.graphml('start.graphml', {})"
    cypher-shell -a bolt://localhost:7687 "match (n) detach delete n;"
    cypher-shell -a bolt://localhost:7687 "call apoc.import.graphml('first_graph.graphml', {})"
    cypher-shell -a bolt://localhost:7687 "match (n) return count(n) as number_of_nodes"
  '';
}
