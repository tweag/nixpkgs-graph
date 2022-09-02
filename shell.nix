{ pkgs ? import <nixpkgs> { }
, pkgs1 ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/master.tar.gz")
    { }
}:
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
in
pkgs.mkShell {
  buildInputs = [
    pythonEnv
    my-pip
    neo4j
    # other dependencies needed here
  ];
  shellHook = ''
    PYTHONPATH=${pythonEnv}/${pythonEnv.sitePackages}
    NEO4J_HOME=${neo4j}
    chmod 755 -R $NEO4J_HOME/share/neo4j/
    wget -P $NEO4J_HOME/share/neo4j/plugins/ -nc https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.4.0.1/apoc-4.4.0.1-all.jar
    neo4j start
    # maybe set more env-vars
  '';
}
