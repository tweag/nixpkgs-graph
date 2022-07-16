{
  pkgs ? import (fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/59b5ae59892ff16075bab39a7d6a9c8509b4055f.tar.gz";
    sha256 = "0c9yjk5spc8mkq5rqcql6j8mqmlq62299l3cz29pjvgxwazwwpv0";
  }) {}
}:

with pkgs;

let 
  inherit (pkgs) lib;

  inherit (builtins) tryEval;
  concatString = lib.concatMapStrings (x: (builtins.toString x) + " ");

# Here is the function that we use to extract information from one package. This function takes in a package and returns an attrset. 
# name : the name of the package (key); value : the information of the package in set form
# Note that variables like buildInputs (set or list) need to be converted to string format first. 
# Otherwise, you will encounter various types of errors with `nix-instantiate --eval --json --strict`
  extractInfo = name: value:
    let 
      res = {
        name = (tryEval(if value ? name then value.name else "")).value;
        path = (tryEval(if value ? outPath then value.outPath else "")).value;
        buildInputs = (tryEval(if value ? buildInputs then concatString value.buildInputs else "")).value;
      };
    in 
      res;

in rec {
  info = (lib.mapAttrs extractInfo) pkgs;
}

