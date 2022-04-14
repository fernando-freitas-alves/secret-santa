__all__ = [
    "convert_people_to_initials",
    "convert_pairs_exclusion_to_initials",
    "get_people_in_pairs",
    "get_people_not_in_pairs",
    "get_possible_pairs",
    "get_people_not_in_collection",
    "get_people_not_in_pairs",
]

from typing import FrozenSet, Set

from utils import collection, string


def convert_people_to_initials(people: FrozenSet[str]) -> FrozenSet[str]:
    return frozenset(map(string.extract_initials, people))


def convert_pairs_exclusion_to_initials(
    pair_exclusions: FrozenSet[FrozenSet[str]],
) -> FrozenSet[FrozenSet[str]]:
    return frozenset({convert_people_to_initials(pair) for pair in pair_exclusions})


def get_people_in_pairs(pairs: FrozenSet[FrozenSet[str]]) -> FrozenSet[str]:
    people: Set[str] = set()
    for pair in pairs:
        people |= pair
    return frozenset(people)


def get_people_not_in_collection(
    people: FrozenSet[str], collection: FrozenSet[str]
) -> FrozenSet[str]:
    return frozenset(people - collection)


def get_people_not_in_pairs(
    people: FrozenSet[str], pairs: FrozenSet[FrozenSet[str]]
) -> FrozenSet[str]:
    people_in_pairs = get_people_in_pairs(pairs)
    return people - people_in_pairs


def get_possible_pairs(
    people: FrozenSet[str], pair_exclusions: FrozenSet[FrozenSet[str]]
) -> FrozenSet[FrozenSet[str]]:
    pairs = collection.create_pairs(people)
    return pairs - pair_exclusions
