# nixpkgs-graph
The main purpose of this project will be to extract the nodes and edge relationships from nixpkgs to build a database. Then generate graph based on this datebase.

## Generate Database
### 1. Node in nixpkgs
The procedures for generating information about the nodes have all been integrated into the `build.sh` file. The corresponding files will appear in the `rawdata/` folder. The following is a description of the methods.

For the first version we use the command `nix search` to find information about all the packages in `nixpkgs` and we output the results in `json` format. This allows us to get a list of pnames and a brief description of all packages under nixpkgs.

After that, we can use the `NodeFormatTrans.py` program to convert the json file into csv format to facilitate the generation of graph nodes. 