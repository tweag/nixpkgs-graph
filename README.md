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
    <a href="LINK FOR DEMO HERE">View Demo</a>
    ·
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

The executable files of this project mainly includes `shell` files and `python` files. where the python file is run independently via nix-shell. Therefore, there is no requirement for the python interpreter in the user's environment, just install `Nix`.

* Nix
  ```sh
  curl -L https://nixos.org/nix/install | sh
  ```

### Installation

**1. Generate Database**

The procedures for generating information about the nodes and edges have all been integrated into the `build.sh` file. The corresponding files will appear in the `rawdata/` folder which is named `nodes.json`.

Each name/value pair in the json file represents a package under `nixpkgs`, and it contains the following information :
- `id`: full name with version of the package under `nixpkgs`, 
- `pname`
- `version`
- `package` : path to which the package belongs (like `[ nixpkgs python3Package ]`)
- `buildInputs` of the package in which each buildInput has the `/nix/store/hash-name(-dev)` structure, so we can identifier the node by `name`.
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
    "type":"node",
    "version": "1.5.1.0"
  }
```
So, according to the `nodes.json` file we get the node and edge information at the same time. The method we use here is to  iterate on the attributes of the root attribute set of nixpkgs using [mapAttrs](https://nixos.org/manual/nix/stable/expressions/builtins.html#builtins-mapAttrs) and merge the `buildInputs` information obtained with the [concatMapStrings](http://ryantm.github.io/nixpkgs/functions/library/strings/) function. Afterwards, we retrieve the desired set via [lib.collect](https://teu5us.github.io/nix-lib.html#lib.attrsets.collect) to eliminate different levels (e.g. the two examples above are at different levels in the original data `{chromium:{...}, python3Packages:{..., zstd:{...}, ...}}`). Finally we use `--json --strict` attribute of `nix-instantiate` to output.
<p align="right">(<a href="#top">back to top</a>)</p>

**2. Generate Graph**

The procedures for generating graph have also been integrated into the `build.sh` file. The corresponding files will appear in the rawdata/ folder which are named `first_graph.png` & `nodes.csv`.

For the first version of the graph, we used [pandas](https://pandas.pydata.org/) of python to process the json format data, and [networkx](https://networkx.org/) to build the graph. The entire program is contained in the `graph.py` file, and the corresponding `requirements.txt` file is provided. However, the python file will be run via `nix-shell`, so there is no need to use the user's native python interpreter. And there is no requirement for user's python environment.

The `graph.py` file contains the following steps:

1. Pre-processing of data:
    - Use `pandas` to read the json file, remove duplicate items and reorder the columns.  
    - Split `buildInputs` (one single string) and extract the `id` part from each buildInput.
    - Add `group` attribute (int) to each node according to their `package` path. For example: the group of a package directly under `nixpkgs` is 1, the one under `python3Package` could be 2.

2. Add nodes:
      
      Add all nodes to the graph (including `id`, `pname`,`version`, `group`).

3. Add edges:
      
      Iterate through all the data read by `pandas` row by row. Set `row.id` as `source` and each `row.buildInput` as `target` and add all such edges into graph.

4. Complete data:

      Since not all packages in `nixpkgs` can be evaluated, there exists a part of nodes contained in the edges in step 3 that were not added in step 2. So additional `group` attributes need to be added for these nodes. Here, the group attribute of all nodes that cannot be evaluated is set to 0.

5. Generate graph picture in `.png` format (random layout)

6. Output the final data in `.csv` format


<!-- USAGE EXAMPLES -->
## Usage

<!-- Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_ -->

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap
- [x] Get basic information
    - [x] Get node information
    - [x] Get edge information
- [ ] Construct Database
- [ ] Construct Graph
- [ ] Analyse

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

Project Link: [https://https://github.com/tweag/nixpkgs-graph](https://https://github.com/tweag/nixpkgs-graph)

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
