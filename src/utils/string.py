__all__ = [
    "extract_initials",
    "convert_str_to_iterable",
    "remove_comments",
    "remove_multiple_white_spaces",
    "split_gen",
]

import re
from typing import Iterable, Optional

PATTERN_COMMENT = re.compile(r"#.*")


def extract_initials(name: str, num_words: Optional[int] = None) -> str:
    name = remove_multiple_white_spaces(name)
    words = name.split()[:num_words]
    initials = [word[0] for word in words]
    return "".join(initials)


def convert_str_to_iterable(
    string: str, /, separator: str = ",", strip_whitespaces: bool = True
) -> Iterable[str]:
    values = split_gen(string, separator=separator)
    if strip_whitespaces:
        return (value.strip() for value in values)
    else:
        return values


def remove_comments(string: str, /) -> str:
    return re.sub(PATTERN_COMMENT, "", string)


def remove_multiple_white_spaces(sentence: str) -> str:
    return " ".join(sentence.split())


def split_gen(string: str, /, separator: str = r"\s+") -> Iterable[str]:
    if separator == "":
        return (c for c in string)
    else:
        pattern = re.compile(f"(?:^|{separator})((?:(?!{separator}).)*)")
        return (match.group(1) for match in re.finditer(pattern=pattern, string=string))
