import os
import sys
from collections.abc import Generator

from dotenv import load_dotenv

load_dotenv()


def input_reader() -> Generator[str, None, None]:
    with open('input.txt', 'r') as file:
        for line in file:
            yield line.strip()


def get_part() -> int:
    try:
        part = int(sys.argv[1])
    except IndexError:
        part = os.environ['LEVEL']
    return part
