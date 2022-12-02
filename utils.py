import sys
from collections.abc import Generator


def input_reader() -> Generator[str, None, None]:
    with open('input.txt', 'r') as file:
        for line in file:
            yield line.strip()


def get_part() -> int:
    try:
        part = int(sys.argv[1])
    except IndexError:
        part = 1
    return part
