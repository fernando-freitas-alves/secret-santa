__all__ = [
    "read_pair_exclusions",
    "read_people",
]

from typing import FrozenSet

from rules import people_rules
from utils import file


def read_pair_exclusions(
    filename: str,
    remove_comments: bool = False,
    strip_whitespaces: bool = False,
    only_initials: bool = False,
) -> FrozenSet[FrozenSet[str]]:
    pair_exclusions = frozenset(
        file.read_matrix_from_file(
            filename=filename,
            remove_comments=remove_comments,
            strip_whitespaces=strip_whitespaces,
        )
    )
    if only_initials:
        pair_exclusions = people_rules.convert_pairs_exclusion_to_initials(
            pair_exclusions
        )

    return pair_exclusions


def read_people(
    filename: str,
    remove_comments: bool = False,
    strip_whitespaces: bool = False,
    only_initials: bool = False,
) -> FrozenSet[str]:
    people = frozenset(
        file.read_lines_from_file(
            filename=filename,
            remove_comments=remove_comments,
            strip_whitespaces=strip_whitespaces,
        )
    )
    if only_initials:
        people = people_rules.convert_people_to_initials(people)

    return people
