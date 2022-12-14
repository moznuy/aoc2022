from __future__ import annotations

import os
import sys
from collections.abc import Generator

from dotenv import load_dotenv

load_dotenv()


def input_reader(
    empty_string: bool = True, strip: bool = True, chars: str | None = None
) -> Generator[str, None, None]:
    with open("input.txt", "r") as file:
        for line in file:
            if strip:
                line = line.strip(chars)
            if empty_string or line:
                yield line


def get_level() -> int:
    try:
        part = int(sys.argv[1])
    except IndexError:
        part = int(os.environ["LEVEL"])
    return part
