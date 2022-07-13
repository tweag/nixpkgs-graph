{
  pkgs ? import (fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/59b5ae59892ff16075bab39a7d6a9c8509b4055f.tar.gz";
    sha256 = "0c9yjk5spc8mkq5rqcql6j8mqmlq62299l3cz29pjvgxwazwwpv0";
  }) {}
}:

with pkgs;

let 
  inherit (pkgs) lib;
  tryEval = builtins.tryEval;

# Here is the function that we use to extract information from one package
# name : the name of the package (key)
# value : the information of the package in set form
# This function takes in a package and returns an attrset 
  extractInfo = name: value:
    let 
      res = builtins.tryEval (
      {
        name = name; 
        version = if value ? name then value.name else "";
        path = if value ? outPath then value.outPath else "" ;
        buildInputs = if value ? buildInputs then value.buildInputs else "";
      });
    in 
      if res.success then res.value 
      else {name = name; version = ""; outPath=""; buildInputs = [];}; 

in rec {

  info = (lib.mapAttrs extractInfo) pkgs;
  info1 = extractInfo ''pkgs'' pkgs.anbox; 
}

