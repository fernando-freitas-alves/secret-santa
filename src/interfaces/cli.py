#!/usr/bin/env python

__all__ = [
    "run",
]

from pprint import pprint
from typing import Any, Collection

import click

from rules import main


def print_collection(collection: Collection[Any], /, name: str) -> None:
    print(f"{name}({len(collection)}) = ")
    pprint(sorted(collection))


@click.command(
    name="amigo-secreto",
    short_help="Amigo secreto",
)
# Filename containing people names
@click.argument(
    "people_filename",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
)
# Filename containing people name pairs that cannot go together
@click.argument(
    "pair_exclusions_filename",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
)
@click.option(
    "-i",
    "--only-initials",
    is_flag=True,
    help="Initials are processed instead of full names",
    default=False,
    show_default=True,
)
@click.option(
    "-c",
    "--remove-comments",
    is_flag=True,
    help="Strip comments (any text starting with '#') from files",
    default=False,
    show_default=True,
)
@click.option(
    "-w",
    "--strip-whitespaces",
    is_flag=True,
    help="Strip leading and trailing whitespaces from files",
    default=False,
    show_default=True,
)
def run(
    people_filename: str,
    pair_exclusions_filename: str,
    only_initials: bool,
    remove_comments: bool,
    strip_whitespaces: bool,
) -> None:
    graph = main.generate_graph(
        people_filename=people_filename,
        pair_exclusions_filename=pair_exclusions_filename,
        only_initials=only_initials,
        remove_comments=remove_comments,
        strip_whitespaces=strip_whitespaces,
    )

    print_collection(graph.pairs, name="possible pairs")
    print_collection(graph.path, name="path")
    print_collection(graph.people, name="people")
    print_collection(graph.path_people, name="people in the path")

    people_not_in_possible_pairs = list(graph.people_not_in_pairs)
    if len(people_not_in_possible_pairs) != 0:
        print(
            "WARNING: The following people are not included in any possible pair: "
            f"{people_not_in_possible_pairs}"
        )

    people_not_in_path = list(graph.people_not_in_path)
    if len(people_not_in_path) != 0:
        print(
            "WARNING: The following people are not included in the solution: "
            f"{people_not_in_path}"
        )

    people_with_single_connection = list(graph.people_with_single_connection)
    if len(people_with_single_connection) != 0:
        print(
            "WARNING: The following people may not give or receive any gift: "
            f"{people_with_single_connection}"
        )

    graph.show()
