import os
import sys
from typing import Optional
from .nixpkgs_graph import graph
from .nixpkgs_analysis import general_info
import click
import subprocess
import pathlib
from contextlib import closing


@click.group()
def cli():
    pass


@cli.command()
# FIXME commented because we have not yet implemented the ability to generate nixpkgs with commit.
# @click.option("-c", "--commit", "commit", default="0000", help="The commit of nixpkgs to be used.") # noqa: E501
@click.option(
    "--rev",
    "rev",
    required=True,
    help="The revision to create url link ('https://github.com/NixOS/nixpkgs/archive/${REVISION}.tar.gz') for fetchTarball to get nixpkgs. There are two options: nixos version or commit. For nixos version you can use keywords like 'master', 'nixos-22.05'. And if you want to use a special commit of nixpkgs, use its full, 40-character SHA-1 hash.",  # noqa: E501
)
@click.option(
    "--sha256",
    "sha256",
    required=True,
    help='The corresponding SHA256 hash if you want to use a commit of nixpkgs. You can create it using \'$ nix-prefetch-url --unpack "https://github.com/NixOS/nixpkgs/archive/${REVISION}.tar.gz"',  # noqa: E501
)
@click.option(
    "--output",
    "output",
    help="The file path used to store the result. If not specified, output to stdout.",
)
def build(rev: str, sha256: str, output: Optional[str]):
    # create parent folder of the output if output is a file
    if output is not None:
        output_folder = pathlib.Path(output).parent
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    nixpkgs_graph_nix_file_path = (
        pathlib.Path(__file__).parent.joinpath("nixpkgs_graph.nix").resolve()
    )

    output_file = open(output, "w") if output is not None else sys.stdout
    with closing(output_file) as f:
        subprocess.run(
            args=[
                "nix-instantiate",
                "--eval",
                "--json",
                "--strict",
                "--show-trace",
                str(nixpkgs_graph_nix_file_path),
                "-A",
                "info",
                "--argstr",
                "pkgs_url",
                f"https://github.com/NixOS/nixpkgs/archive/{rev}.tar.gz",
                "--argstr",
                "sha256",
                sha256,
            ],
            stdout=f,
        )


@cli.command()
@click.option(
    "--input-file",
    "input_file",
    required=True,
    help="The path to the input json file with node information.",
)
@click.option(
    "--output-folder",
    "output_folder",
    required=True,
    help="The folder path used to store results.",
)
@click.option(
    "--mode",
    "mode",
    type=click.Choice(["buildInputs", "propagatedBuildInputs", "both"]),
    default="both",
    help="Select the type of edges to be added to the graph. Can be 'buildInputs', 'propagatedBuildInputs' or 'both'. Default is 'both'.",  # noqa: E501
)
@click.option(
    "-t", "--title", "title", default="first_graph", help="Title of the graph picture"
)
@click.option(
    "-a",
    "--arrows",
    "arrows",
    is_flag=True,
    help="When used, draw arrowheads with FancyArrowPatches (bendable and stylish), else draw edges using LineCollection (linear and fast)",  # noqa: E501
)
@click.option("-n", "--node-size", "node_size", default=0.1, help="Size of nodes.")
@click.option(
    "-e", "--edge-width", "edge_width", default=0.01, help="Line width of edges."
)
def generate_graph(
    input_file: str,
    output_folder: str,
    mode: str,
    title,
    arrows,
    node_size,
    edge_width,
):
    click.echo()
    click.echo(f"The graph will be generated from '{input_file}' with :")
    click.echo(f"- title: {title}")
    click.echo(f"- arrows: {arrows}")
    click.echo(f"- node size: {node_size}")
    click.echo(f"- edge width: {edge_width}")
    click.echo(f"- mode: '{mode}'")
    click.echo()
    click.echo(f"The final results will be saved in the folder {output_folder}.")
    nxG = graph(input_file, output_folder, title, arrows, node_size, edge_width, mode)
    general_info(nxG, output_folder)


cli()
