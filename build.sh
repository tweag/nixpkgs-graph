nix search --json nixpkgs >rawdata/nodes.json
./node_format_trans.py
