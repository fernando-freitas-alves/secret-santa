__all__ = [
    "create_pairs",
]

from itertools import combinations
from typing import Any, FrozenSet, Iterable


def create_pairs(iterable: Iterable[Any]) -> FrozenSet[FrozenSet[Any]]:
    pairs = combinations(iterable, r=2)
    return frozenset((frozenset(pair) for pair in pairs))
