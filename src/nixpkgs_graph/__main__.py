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
    "-r",
    "--file-read-path",
    "file_read_path",
    default="./rawdata/nodes.json",
    help="The path to read the json file of node information, default is './rawdata/nodes.json' ",
)
@click.option(
    "-f",
    "--file-save-folder",
    "file_save_folder",
    default="./rawdata/",
    help="The folder path used to store results, ending with /, default is './rawdata/'",
)
@click.option(
    "-t", "--title", "title", default="first_graph", help="Title of the graph picture"
)
@click.option(
    "-a",
    "--arrows",
    "arrows",
    default=False,
    help="If True, draw arrowheads with FancyArrowPatches (bendable and stylish). If False, draw edges using LineCollection (linear and fast)",  # noqa: E501
)
@click.option("-n", "--node-size", "node_size", default=0.1, help="Size of nodes.")
@click.option(
    "-e", "--edge-width", "edge_width", default=0.01, help="Line width of edges."
)
@click.option(
    "-m",
    "--mode",
    "mode",
    default=2,
    help="Select the type of edges to be added to the graph. 0: buildInputs, 1: promotedBuildInputs, 2: both.",  # noqa: E501
)
def generate_graph(
    file_read_path, file_save_path, title, arrows, node_size, edge_width, mode
):
    click.echo("\nThe graph will be generated from '%s' with :" % file_read_path)
    click.echo("- title: %s" % title)
    click.echo("- arrows: %s" % arrows)
    click.echo("- node size: %f" % node_size)
    click.echo("- edge width: %f" % edge_width)
    click.echo("- mode: '%d'" % mode)
    click.echo("\nThe final results will be saved in the folder '%s'." % file_save_path)
    nxG = graph(
        file_read_path, file_save_path, title, arrows, node_size, edge_width, mode
    )
    general_info(nxG, file_save_path)


cli()
