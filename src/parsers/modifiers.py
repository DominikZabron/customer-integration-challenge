import re
from functools import partial

from .validators import is_digit

fill_none = lambda x: None if not x else x
negative_to_zero = lambda x: 0 if x and int(x) < 0 else x
to_int = lambda x: int(x) if x and is_digit(x) else x


def shrink_on_char(x, char: str):
    try:
        return x[: x.index(char)].strip()
    except (ValueError, AttributeError):
        return x


shrink_on_hash = partial(shrink_on_char, char="#")


def shrink_on_chars(x, char: str, occurences: int = 3):
    try:
        if match := re.search(f"[{re.escape(char)}]{{{occurences},}}", x):
            return x[: match.start()].strip()
    except TypeError:
        return x
    return x


shrink_on_spaces = partial(shrink_on_chars, char=" ", occurences=3)
