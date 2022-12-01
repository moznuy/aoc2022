from collections.abc import Generator


def input_reader() -> Generator[str, None, None]:
    with open('input.txt', 'r') as file:
        for line in file:
            yield line.strip()
