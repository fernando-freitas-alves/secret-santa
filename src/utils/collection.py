__all__ = [
    "create_pairs",
]

from itertools import combinations
from typing import FrozenSet, Iterable


def create_pairs(iterable: Iterable[str]) -> FrozenSet[FrozenSet[str]]:
    pairs = combinations(iterable, r=2)
    return frozenset((frozenset(pair) for pair in pairs))
