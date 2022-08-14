from .nixpkgs_graph import graph
from .nixpkgs_analysis import general_info
import click


@click.command()
@click.option(
    "-r",
    "--file-read-path",
    "file_read_path",
    default="./rawdata/nodes.json",
    help="The path to read the json file of node information, default is './rawdata/nodes.json' ",
)
@click.option(
    "-s",
    "--file-save-path",
    "file_save_path",
    default="./rawdata/",
    help="The folder path used to store the graph picture, ending with /, default is be './rawdata/'",
)
@click.option(
    "-t", "--title", "title", default="first_graph", help="Title of the graph picture"
)
@click.option(
    "-a",
    "--arrows",
    "arrows",
    default=False,
    help="If True, draw arrowheads with FancyArrowPatches (bendable and stylish). If False, draw edges using LineCollection (linear and fast)",
)
@click.option("-n", "--node-size", "node_size", default=0.1, help="Size of nodes.")
@click.option(
    "-e", "--edge-width", "edge_width", default=0.01, help="Line width of edges."
)
def generate_graph(
    file_read_path, file_save_path, title, arrows, node_size, edge_width
):
    click.echo("\nThe graph will be generated from '%s' with :" % file_read_path)
    click.echo("- title: %s" % title)
    click.echo("- arrows: %s" % arrows)
    click.echo("- node size: %f" % node_size)
    click.echo("- edge width: %f" % edge_width)
    click.echo("\nThe final results will be saved in the folder '%s'." % file_save_path)
    nxG = graph(file_read_path, file_save_path, title, arrows, node_size, edge_width)
    general_info(nxG)


generate_graph()
