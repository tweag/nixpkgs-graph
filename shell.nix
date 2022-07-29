{ pkgs ? import <nixpkgs> { } }:
let
  my-python = pkgs.python3;
  my-pip = pkgs.python3Packages.pip;
  pythonEnv = my-python.withPackages (p: with p;
    [
      matplotlib
      networkx
      pandas
      scipy
      setuptools
      # other python packages needed here
    ]);
in
pkgs.mkShell {
  buildInputs = [
    pythonEnv
    my-pip
    # other dependencies needed here
  ];
  shellHook = ''
    PYTHONPATH=${pythonEnv}/${pythonEnv.sitePackages}
    # maybe set more env-vars
  '';
}
