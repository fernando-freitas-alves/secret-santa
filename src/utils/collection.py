__all__ = [
    "create_pairs",
    "get_non_repeated_items",
]

from itertools import combinations
from typing import Any, FrozenSet, Iterable, Set


def create_pairs(iterable: Iterable[Any]) -> FrozenSet[FrozenSet[Any]]:
    pairs = combinations(iterable, r=2)
    return frozenset((frozenset(pair) for pair in pairs))


def get_non_repeated_items(iterable: Iterable[Any]) -> FrozenSet[Any]:
    repeated: Set[Any] = set()
    non_repeated: Set[Any] = set()
    for item in iterable:
        if item in non_repeated:
            repeated.add(item)
            non_repeated.remove(item)
        else:
            non_repeated.add(item)
    return frozenset(non_repeated)
