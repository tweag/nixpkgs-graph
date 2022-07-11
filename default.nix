{
  pkgs ? import (fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/59b5ae59892ff16075bab39a7d6a9c8509b4055f.tar.gz";
    sha256 = "0c9yjk5spc8mkq5rqcql6j8mqmlq62299l3cz29pjvgxwazwwpv0";
  }) {}
}:

with pkgs;

let 
  lib = pkgs.lib;

  concatString = lib.concatMapStrings (x: (builtins.toString x) + " ");

  getInfo = lib.mapAttrs (name: value:
    let 
      res = builtins.tryEval (
      ''${name}, '' + 
      ''${if value ? name then value.name else ""}, '' + 
      ''${if value ? outPath then value.outPath else ""}, '' +
      ''${if value ? buildInputs then (concatString value.buildInputs) else ""}'');
    in 
      if res.success then res.value else ''${name}, , ,''
    );

  concatInfo = lib.concatMapStrings (x: x + "\n");
in rec {
  inherit pkgs;
  info = getInfo pkgs;
  file = concatInfo (pkgs.lib.attrValues info);
}


