# `nixpkgs-graph`

Build a graph database of nixpkgs.

## About

This project aims at building a graph database of `nixpkgs`.
Read more on our blog post: ["Construction and analysis of the build and runtime dependency graph of Nixpkgs"](https://www.tweag.io/blog/2022-09-13-nixpkgs-graph/).

## Usage

### Requirements

* [Nix](https://nixos.org/)

### Using `build.sh`

```sh
./build.sh 481f9b246d200205d8bafab48f3bd1aeb62d775b 0n6a4a439md42dqzzbk49rfxfrf3lx3438i2w262pnwbi3dws72g 
```

where

* the first argument is the revision (the 40-character SHA-1 hash) of a commit
* the second is the [SHA256](https://wiki.nixos.org/wiki/How_to_fetch_Nixpkgs_with_an_empty_NIX_PATH) hash of its content (same as `nix-prefetch-url --unpack`).

After running this script you will find in the `./rawdata/` folder:

- `nodes.json`: raw data extracted with the Nix evaluation
- `nodes.csv`: structured data which can be loaded by most tools
- `first_graph.png`: image drawn with networkx
- `first_graph.gexf`: data which can be loaded by Gephi
- `first_graph.grapgml`: data which can be loaded by Neo4j
- `general_info.json`: some basic information (number of nodes, number of edges)

If you want to query the graph with Neo4j using [Cypher Shell](https://neo4j.com/docs/operations-manual/current/tools/cypher-shell/), a `shell.nix` is provided:

```sh
$ nix-shell
[nix-shell]$ cypher-shell -a bolt://localhost:7687 "MATCH (n) RETURN COUNT(n) as number_of_nodes;"
```

### Manual steps

1. The provided Nix shell also create a Python virtual environment:
   
   ```sh
   nix-shell --command "exit"
   source .venv/bin/activate
   ```

2. Run `nixpkgs_graph` in the command line:
  
   ```sh
   python3 -m nixpkgs_graph --help
   ```

   To get the nixpkgs database in json format, you can use the following code:
   
   ```sh
   python3 -m nixpkgs_graph build --rev 481f9b246d200205d8bafab48f3bd1aeb62d775b --sha256 0n6a4a439md42dqzzbk49rfxfrf3lx3438i2w262pnwbi3dws72g
   ```
   
   The `-rev` flag means revision, which is the 40-character SHA-1 hash of a commit.
   And `-sha256` is its [SHA256](https://wiki.nixos.org/wiki/How_to_fetch_Nixpkgs_with_an_empty_NIX_PATH) hash.

3. Generate the graph and do some basic analysis:
   
   ```sh
   python3 -m nixpkgs_graph generate-graph --input-file INPUT_FILE --output-folder OUTPUT_FOLDER
   ```
   
   The input file should be the path to the data extracted in the previous step.

5. To use Neo4j to query the graph:
   
   - Find the `.graphml` format file in the output folder.
   - Copy it to the import folder of Neo4j `$NEO4J_HOME/share/neo4j/import/`.
   - Clear the original graph to avoid duplication:
   
     ```sh
     cypher-shell -a bolt://localhost:7687 "MATCH (n) DETACH DELETE n;"
     ```
   - Use `APOC` to import it:
     
     ```sh
     cypher-shell -a bolt://localhost:7687 "call apoc.import.graphml('<filename>.graphml', {})"
     ```
     
     Or in Neo4j browser if you use desktop version:
     
     ```sh
     call apoc.import.graphml('<filename>.graphml', {})
     ```

- Use some simple commands to test if the graph is successfully imported:

  ```sh
  cypher-shell -a bolt://localhost:7687 "MATCH (n) RETURN n LIMIT 10;"
  ```

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contacts

Eloi Xuan WANG - [@GearlessJohn](https://github.com/GearlessJohn) - xuan.wang@polytechnique.edu 

Guillaume Desforges - [@GuillaumeDesforges](https://github.com/GuillaumeDesforges) - guillaume.desforges@tweag.io

Project Link: [https://github.com/tweag/nixpkgs-graph](https://github.com/tweag/nixpkgs-graph)

## Appendix

The following are details about the methods used.

### How data is extracted

Each name/value pair in the JSON file represents a package under `nixpkgs`, and it contains the following information :

- `id`: full name with version of the package under `nixpkgs`, 
- `pname`
- `version`
- `package` : path to which the package belongs (like `[ nixpkgs python3Package ]`)
- `buildInputs` of the package in which each buildInput has the `/nix/store/hash-name(-dev)` structure, so we can identifier the node by `name`.
- `propagatedBuildInputs` of the package in which each propagatedBuildInput has also the `/nix/store/hash-name(-dev)` structure, so we can still identifier the node by `name`.
- `type = "node"` which is used as an identification marker for lib.collect

Example : 

```json
{
  "buildInputs": "/nix/store/c1pzk30ksbff1x3krxnqzrzzfjazsy3l-gsettings-desktop-schemas-42.0 /nix/store/mmwc0xqwxz2s4j35w7wd329hajzfy2f1-glib-2.72.3-dev /nix/store/64mp60apx1klb14l0205562qsk1nlk39-gtk+3-3.24.34-dev /nix/store/6hdwxlycxjgh8y55gb77i8yqglmfaxkp-adwaita-icon-theme-42.0 ",
  "id": "chromium-103.0.5060.134",
  "package": [
    "nixpkgs",
    "chromium"
  ],
  "pname": "chromium",
  "propagatedBuildInputs":"",
  "type":"node",
  "version": "103.0.5060.134"
}
```

and another example of depth 1 under `python3Packages`:

```json
{
    "buildInputs": "/nix/store/vakcc74vp08y1rb1rb1cla6885ayklk3-zstd-1.5.2-dev ",
    "id": "python3.9-zstd-1.5.1.0",
    "package": [
      "nixpkgs",
      "python3Packages",
      "zstd"
    ],
    "pname": "zstd",
    "propagatedBuildInputs":"/nix/store/xpwwghl72bb7f48m51amvqiv1l25pa01-python3-3.9.13 ",
    "type":"node",
    "version": "1.5.1.0"
  }
```

To get this data, we evaluate a Nix expression designed to yield all the data we want.
Note that we use `--json --strict` when calling `nix-instantiate`.

The Nix expresison iterates on the key/value pairs of the root attribute set of nixpkgs (and some other selected attribute sets) using [mapAttrs](https://nixos.org/manual/nix/stable/expressions/builtins.html#builtins-mapAttrs).
Afterwards, we retrieve the desired sets via [lib.collect](https://teu5us.github.io/nix-lib.html#lib.attrsets.collect).


### How raw data is processed

For the first version of the graph, we used [pandas](https://pandas.pydata.org/) to process the raw JSON data and [networkx](https://networkx.org/) to process the graph data.

See `nixpkgs_graph.py`

### Analyzing data

Use the `networkx.read_gexf()` function to read the `.gexf` file.

This project provides some basic infomatation:

- number of nodes
- number of edges
- top 10 nodes which have the largest number of dependencies
- top 10 most cited nodes
- average number of dependencies of a derivation
- cycles in the nixpkgs graph
- length of the longest path in the graph

### Visualizing the graph

Use `Gephi` to read and process the generated `.gexf` for visualization.

