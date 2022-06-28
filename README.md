# nixpkgs-graph
The main purpose of this project will be to extract the nodes and edge relationships from nixpkgs to build a database. Then generate graph based on this datebase.

## Generate Database

For the first version we use the command:
```
$ nix search --json nixpkgs > nodes.json
```

This allows us to get a list and a brief description of all packages under nixpkgs.
After that, we can use the `Tocsv.py` program to convert the json file into csv format to facilitate the generation of graph nodes.

All of the above steps have been included in `build.sh`. The corresponding files will appear in the `rawdata/` folder.