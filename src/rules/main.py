__all__ = [
    "generate_graph",
]

from interfaces import files
from interfaces.graph import Graph
from rules import people_rules


def generate_graph(
    people_filename: str,
    pair_exclusions_filename: str,
    only_initials: bool = False,
    remove_comments: bool = False,
    strip_whitespaces: bool = False,
) -> Graph:
    people = files.read_people(
        filename=people_filename,
        remove_comments=remove_comments,
        strip_whitespaces=strip_whitespaces,
        only_initials=only_initials,
    )
    pair_exclusions = files.read_pair_exclusions(
        filename=pair_exclusions_filename,
        remove_comments=remove_comments,
        strip_whitespaces=strip_whitespaces,
        only_initials=only_initials,
    )
    possible_pairs = people_rules.get_possible_pairs(
        people=people,
        pair_exclusions=pair_exclusions,
    )
    return Graph(pairs=possible_pairs)
