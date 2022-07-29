{ pkgs ? import <nixpkgs> { } }:
let
  my-python = pkgs.python3;
  pythonEnv = my-python.withPackages (p: with p; [
    # other python packages needed here
  ]);
in
pkgs.mkShell {
  buildInputs = [
    pythonEnv
    # other dependencies needed here
  ];
  shellHook = ''
    PYTHONPATH=${pythonEnv}/${pythonEnv.sitePackages}
    # maybe set more env-vars
  '';
}
