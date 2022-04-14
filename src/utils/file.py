__all__ = [
    "read_lines_from_file",
    "read_matrix_from_file",
]

import os
from typing import FrozenSet, Iterable

from utils import string


def read_lines_from_file(
    filename: str,
    strip_whitespaces: bool = False,
    remove_comments: bool = False,
) -> Iterable[str]:
    with open(filename) as file:
        for line in file:
            line = line.rstrip(os.linesep)
            if strip_whitespaces:
                line = line.strip()
            if remove_comments:
                line = string.remove_comments(line)
            if not line:
                continue
            yield line


def read_matrix_from_file(
    filename: str,
    separator: str = ",",
    strip_whitespaces: bool = False,
    remove_comments: bool = False,
) -> Iterable[FrozenSet[str]]:
    lines = read_lines_from_file(filename)
    for line in lines:
        if remove_comments:
            line = string.remove_comments(line)
        values = string.convert_str_to_iterable(
            line, separator=separator, strip_whitespaces=strip_whitespaces
        )
        yield frozenset(values)
