{ pkgs_url ? "https://github.com/NixOS/nixpkgs/archive/nixos-22.05.tar.gz"
}:

with pkgs_url;

let
  pkgs = import (fetchTarball pkgs_url) { };

  inherit (pkgs) lib;

  inherit (builtins) tryEval;
  concatString = lib.concatMapStrings (x: (builtins.toString x) + " ");

  # This is a white list of packages used for recursion.
  packages = [
    "darwinPackages"
    "haskellPackages"
    "dotnetPackages"
    "emacsPackages"
    "emscriptenPackages"
    "javaPackages"
    "luaPackages"
    "ocamlPackages"
    "perlPackages"
    "phpPackages"
    "pythonPackages"
    "python3Packages"
    "unixTools"
    "winePackages"
  ];

  # Here is the function that we use to extract information from one package. This function takes in a package and returns an attrset. 
  # @name : the name of the package (key); @value : the information of the package in set form
  # Note that variables like buildInputs (set or list) need to be converted to string format first. 
  # Otherwise, you will encounter various types of errors with `nix-instantiate --eval --json --strict`
  # We can use lib.strings.splitString to convert the long string into list but nix is not efficient enough.
  extractInfo = depth: packagePath:
    lib.mapAttrs (name: value:
      let
        res = tryEval (if lib.isDerivation value then rec {
          type = "node";
          pname = (tryEval (if value ? pname then value.pname else "")).value;
          version =
            (tryEval (if value ? version then value.version else "")).value;
          package = packagePath ++ [ pname ];
          id = (tryEval (if value ? name then value.name else "")).value;
          buildInputs = (tryEval (if value ? buildInputs then
            concatString value.buildInputs
          else
            "")).value;
          propagatedBuildInputs = (tryEval
            (if value ? propagatedBuildInputs then
              concatString value.propagatedBuildInputs
            else
              "")).value;
          # FIXME commented because it does not evaluate, raises error "attribute 'linux_py_27_cpu' missing"
          # nativeBuildInputs = (tryEval (if value ? nativeBuildInputs then concatString value.nativeBuildInputs else "")).value;
          # propagatedNativeBuildInputs = (tryEval (if value ? propagatedNativeBuildInputs then concatString value.propagatedNativeBuildInputs else "")).value;
        } else if ((value.recurseForDerivations or false
          || value.recurseForRelease or false) || ((builtins.typeOf value)
          == "set" && builtins.elem name packages && depth < 1)) then
          extractInfo (depth + 1) (packagePath ++ [ name ]) value
        else
          null);
      in
      if res.success then res.value else null);

in
rec {
  info = lib.collect (x: (x.type or null) == "node")
    (extractInfo 0 [ "nixpkgs" ] pkgs);
}
