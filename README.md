<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/tweag/nixpkgs-graph">
     <h1 align="center">Nixpkgs-Graph</h1>
  </a>
  <p align="center">
    A nixpkgs content database with graph building!
    <br />
    <a href="LINK FOR BLOG HERE"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/tweag/nixpkgs-graph/issues">Report Bug</a>
    ·
    <a href="https://github.com/tweag/nixpkgs-graph/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#appendix">Appendix</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About Nixpkgs-Graph

`Nix` is a package manager that utilizes a purely functional deployment model which advertises more reliable, reproducible, and portable packages. And `nixpkgs` is a collection of software packages that can be installed with the Nix package manager.

The main purpose of this project will be to extract the nodes and edge relationships from nixpkgs to build a database. Then generate graph based on this datebase.

Here's why:
* Nixpkgs contains more than forty thousand software packages, covering a very wide range. So as a database for studying the relationships between software packages, nixpkgs is excellent.
* As computer technology continues to accumulate, the issue of software ecology is growing in importance. Constructing visual images through dependencies between software packages can show some macro features.

Use the `README.md` to get started.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

This section list the major frameworks/libraries used to bootstrap the project. 

* [Nix](https://https://nixos.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Nix

The executable files of this project mainly includes `nix` files and `python` files. where the python file is run independently via nix-shell. Therefore, there is no requirement for the python interpreter or other softwares in the user's environment, just install `Nix`.
```sh
$ curl -L https://nixos.org/nix/install | sh
```

### Installation

A `shell.nix` file is provided to implement all the required installation steps, so you just need to run:
```sh
$ nix-shell
```

<!-- USAGE EXAMPLES -->
## Usage

<!-- Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources. -->

### Default mode
After installation, if you just want to follow the default mode to get the data, then after running `nix-shell`, you will find in the `./rawdata/` folder:

- `nodes.json`, raw data we extracted from nixpkgs
- `nodes.csv`, data after we have processed the json file using pandas
- `first_graph.png`, image drawn with networkx
- `first_graph.gexf`, data to be input if you want to use Gephi
- `start.graphml`, special file used to start Neo4j
- `first_graph.graphml`, data to be input if you want to use Neo4j
- `general_info.json`, file containing some basic information (number of nodes, number of edges, etc) about nixpkgs graph

After that you can use the Cypher language to query, like:
```sh
cypher-shell -a bolt://localhost:7687 "MATCH (n) RETURN n LIMIT 10;"
```
[Cypher Shell](https://neo4j.com/docs/operations-manual/current/tools/cypher-shell/) is a command-line tool that comes with the Neo4j distribution.

In particular, if you want to specify the version of nixpkgs, you can use the following two parameters:
```sh
nix-shell --argstr rev <REVISION> --argstr sha256 <SHA256>
```
where the first argument is the revision (the 40-character SHA-1 hash) of a commit and the second is the [SHA256](https://nixos.wiki/wiki/How_to_fetch_Nixpkgs_with_an_empty_NIX_PATH) hash of the commit. You can replace them by the commit you want to use.


### Manual mode

If you want to **manually** adjust some parameters (e.g. output folder), you can use the following steps. 

1. Start by entering the specified virtual environment:
```sh
nix-shell
```

2. You can run `nixpkgs_graph` as a package with the attributes you like:
```sh
python3 -m nixpkgs_graph [OPTIONS] COMMAND [ARGS]
``` 
You can use `--help` flag to read the help information.

3. To get the nixpkgs database in json format, you can use the following code:
```sh
python3 -m nixpkgs_graph build --rev 481f9b246d200205d8bafab48f3bd1aeb62d775b --sha256 0n6a4a439md42dqzzbk49rfxfrf3lx3438i2w262pnwbi3dws72g
```
The `-rev` flag means revision, which is the 40-character SHA-1 hash of a commit. And `-sha256` is its [SHA256](https://nixos.wiki/wiki/How_to_fetch_Nixpkgs_with_an_empty_NIX_PATH) hash. You can replace them with the version you like.

4. Then to generate the graph and do some basic analysis, use:
```sh
python3 -m nixpkgs_graph generate-graph --input-file INPUT_FILE --output-folder OUTPUT_FOLDER
``` 
The input file should be the path to the result you get in step 3. And the output folder is used to store results.

5. Finally, here we provide the method to use Neo4j to access the graph.

- You can find the `.graphml` format file in the output folder. Please copy it to the import folder of Neo4j `$NEO4J_HOME/share/neo4j/import/`.

- Now let's clear the original graph to avoid duplication:
  ```sh
  cypher-shell -a bolt://localhost:7687 "MATCH (n) DETACH DELETE n;"
  ```

- Now use `APOC` to import it:
  ```sh
  cypher-shell -a bolt://localhost:7687 "call apoc.import.graphml('<filename>.graphml', {})"
  ```
  Or in Neo4j browser if you use desktop version:
  ```sh
  call apoc.import.graphml('<filename>.graphml', {})
  ```

- Now you can use some simple commands to test if the graph is successfully imported, like:
  ```sh
  cypher-shell -a bolt://localhost:7687 "MATCH (n) RETURN n LIMIT 10;"
  ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap
- [x] Get basic information
    - [x] Get node information
    - [x] Get edge information
- [x] Construct Database
- [x] Construct Graph
- [x] Analyse
- [x] CLI tool
- [x] Get nixpkgs data to Neo4j

<!-- See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues). -->

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

<!-- Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request -->

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

<!-- Distributed under the MIT License. See `LICENSE.txt` for more information. -->

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Eloi Xuan WANG - [@GearlessJohn](https://github.com/GearlessJohn) - eloi.wang@tweag.io

Guillaume Desforges - [@GuillaumeDesforges](https://github.com/GuillaumeDesforges) - guillaume.desforges@tweag.io

Project Link: [https://github.com/tweag/nixpkgs-graph](https://github.com/tweag/nixpkgs-graph)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

<!-- Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search) -->

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- APPENDIX -->
## Appendix

The following are details about the methods used.

**1. Generate Database**

Each name/value pair in the json file represents a package under `nixpkgs`, and it contains the following information :
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
So, according to the `nodes.json` file we get the node and edge information at the same time. The method we use here is to  iterate on the attributes of the root attribute set of nixpkgs using [mapAttrs](https://nixos.org/manual/nix/stable/expressions/builtins.html#builtins-mapAttrs) and merge the `buildInputs` and `propagatedBuildInputs` information obtained with the [concatMapStrings](http://ryantm.github.io/nixpkgs/functions/library/strings/) function. Afterwards, we retrieve the desired set via [lib.collect](https://teu5us.github.io/nix-lib.html#lib.attrsets.collect) to eliminate different levels (e.g. the two examples above are at different levels in the original data `{chromium:{...}, python3Packages:{..., zstd:{...}, ...}}`). Finally we use `--json --strict` attribute of `nix-instantiate` to output.
<p align="right">(<a href="#top">back to top</a>)</p>

**2. Generate Graph**

For the first version of the graph, we used [pandas](https://pandas.pydata.org/) of python to process the json format data, and [networkx](https://networkx.org/) to build the graph. The entire program is contained in the `nixpkgs_nixpkgs_graph.py` file, and the corresponding `requirements.txt` file is provided. However, the python file will be run via `nix-shell` using the virtual environment `.venv`, so there is no need to use the user's native python interpreter. And there is no requirement for user's python environment.

The `nixpkgs_graph.py` file contains the following steps:

1. Pre-processing of data:
    - Use `pandas` to read the json file, remove duplicate items and reorder the columns.  
    - Split `buildInputs` and `propagatedBuildInputs` (one single string) and extract the `id` part from each buildInput.
    - Add `group` attribute (int) to each node according to their `package` path. For example: the group of a package directly under `nixpkgs` is 1, the one under `python3Package` could be 2.

2. Add nodes:
      
      Add all nodes to the graph (including `id`, `pname`,`version`, `group`).

3. Add edges:
      
      Iterate through all the data read by `pandas` row by row. Set `row.id` as `source` and each `row.buildInput`(or `row.propagatedBuildInputs`) as `target` and add all such edges into graph.

4. Complete data:

      Since not all packages in `nixpkgs` can be evaluated, there exists a part of nodes contained in the edges in step 3 that were not added in step 2. So additional `group` attributes need to be added for these nodes. Here, the group attribute of all nodes that cannot be evaluated is set to 0.

5. Generate graph picture in `.png` format (random layout)

6. Output the final database in `.csv` format and the graph in `.gexf` format.


**3. Analyze Graph**

The analysis of graph mainly includes two parts: one is the analysis of data based on `networkx` and `pandas`, and the other is the visual analysis based on [gephi](https://gephi.org/). The related codes can be found in `nipkgs_analysis.py` file.

***Data Analysis***

You can use the `networkx.read_gexf()` function to read the .gexf file to process the data of the networkx.DiGraph structure by yourself. This project provides some basic infomatation:

- number of nodes
- number of edges
- nodes which have the largest number of dependencies (top10)
- most cited nodes (top10)
- average number of dependencies of a derivation
- simple cycles in the nixpkgs graph
- length of the longest path in the graph

***Visual Analysis***

This program will automatically generate `.gexf` format file and store it in the `rawdata/` folder by default. Users can use `Gephi` to read and process the data for visualization.