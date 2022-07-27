{ pkgs ? import
    (fetchTarball https://github.com/NixOS/nixpkgs/archive/nixos-22.05.tar.gz)
    { }
}:

with pkgs;

let
  inherit (pkgs) lib;

  inherit (builtins) tryEval;
  concatString = lib.concatMapStrings (x: (builtins.toString x) + " ");

  # This is a white list of packages used for recursion.
  packages = [
    "haskellPackages"
    "javaPackages"
    "ocamlPackages"
    "perlPackages"
    "phpPackages"
    # "pythonPackages"
    "python3Packages"
  ];

  # Here is the function that we use to extract information from one package. This function takes in a package and returns an attrset. 
  # @name : the name of the package (key); @value : the information of the package in set form
  # Note that variables like buildInputs (set or list) need to be converted to string format first. 
  # Otherwise, you will encounter various types of errors with `nix-instantiate --eval --json --strict`
  # We can use lib.strings.splitString to convert the long string into list but nix is not efficient enough.
  extractInfo = depth: packagePath: name: value:
    let
      valueEvalResult = tryEval value;
      package = packagePath ++ [ name ];
    in
    if valueEvalResult.success then
      let
        okValue = valueEvalResult.value;
      in
      if lib.isDerivation okValue then
        {
          type = "node";
          inherit package;
          pname = (tryEval (if okValue ? pname then okValue.pname else "")).value;
          version = (tryEval (if okValue ? version then okValue.version else "")).value;
          name = (tryEval (if okValue ? name then okValue.name else "")).value;
          outputPath =
            let pEvalResult = tryEval (toString okValue);
            in if pEvalResult.success then pEvalResult.value else null;
          buildInputs = map
            (p:
              let pEvalResult = tryEval (toString p);
              in if pEvalResult.success then pEvalResult.value else null)
            (okValue.buildInputs or [ ]);
        }
      else if ((okValue.recurseForDerivations or false || okValue.recurseForRelease or false)
        || (lib.isAttrs okValue && builtins.elem name packages && depth < 1)) then
        lib.mapAttrs (extractInfo (depth + 1) (package)) okValue
      else
        null
    else
      null;
in
rec {
  info = lib.collect (x: (x.type or null) == "node") (lib.mapAttrs (extractInfo 0 [ ]) pkgs);
  info1 = lib.collect (x: (x.type or null) == "node") (lib.mapAttrs (extractInfo 0 [ ]) {
    python3Packages = pkgs.python3Packages;
    chromium = pkgs.chromium;
  });
}

