{ pkgs ?
  import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/master.tar.gz")
  { } }:
let neo4j = pkgs.neo4j;
in pkgs.mkShell {
  buildInputs = [
    neo4j
    # other dependencies needed here
  ];
  shellHook = ''
    NEO4J_HOME=${neo4j}
    chmod 755 -R $NEO4J_HOME/share/neo4j/
    wget -P $NEO4J_HOME/share/neo4j/plugins/ -nc https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.4.0.1/apoc-4.4.0.1-all.jar
    neo4j start
    grep ^apoc.import.file.enabled=true $NEO4J_HOME/share/neo4j/conf/neo4j.conf || echo "apoc.import.file.enabled=true" >> $NEO4J_HOME/share/neo4j/conf/neo4j.conf
    grep ^dbms.security.auth_enabled=false $NEO4J_HOME/share/neo4j/conf/neo4j.conf || echo "dbms.security.auth_enabled=false" >> $NEO4J_HOME/share/neo4j/conf/neo4j.conf
    # maybe set more env-vars
  '';
}
