import itertools

import utils


def accommodate_new_rock(chamber: list[str], empty_wall: str, rock: list[str]) -> int:
    empty_walls = 0
    needed_empty_walls = 3 + len(rock)
    for c in reversed(chamber):
        if c == empty_wall:
            empty_walls += 1
        else:
            break

    if needed_empty_walls <= empty_walls:
        return empty_walls - needed_empty_walls
    for _ in range(needed_empty_walls - empty_walls):
        chamber.append(empty_wall)
    return 0


def combine_lines(background: str, new: str, x: int, clear: bool, final: bool) -> tuple[bool, str | None]:
    new_line = []
    new = new if final else new.replace('#', '@')
    for i, b in enumerate(background):
        j = i - x
        if j < 0 or j >= len(new):
            new_line.append(b)
            continue

        r = new[j]
        empty_background = b == '.'
        empty_rock = r == '.'

        if not clear:
            if empty_rock and empty_background:
                new_line.append('.')
                continue
            if empty_rock and not empty_background:
                new_line.append(b)
                continue
            if not empty_rock and empty_background:
                new_line.append(r)
                continue
            if not empty_rock and not empty_background:
                return False, ''
        else:
            if empty_rock and empty_background:
                new_line.append('.')
                continue
            if empty_rock and not empty_background:
                new_line.append(b)
                continue
            if not empty_rock and empty_background:
                assert False
            if not empty_rock and not empty_background:
                new_line.append('.')
                continue
            assert False
    return True, ''.join(new_line)


def fill_rock(chamber: list[str], rock: list[str], x: int, y: int, empty: bool, final: bool = False) -> bool:
    tmp_lines = [combine_lines(chamber[-i - y], line, x, empty, final) for i, line in enumerate(rock)]

    if not all(line[0] for line in tmp_lines):
        return False

    for i, line in enumerate(rock):
        chamber[-i - y] = tmp_lines[i][1]
    return True


def print_chamber(chamber: list[str]):
    for c in reversed(chamber):
        print(c)
    print()


def solution(level):
    line = next(utils.input_reader())
    """
    >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
    >>><<<<<>>
    """
    wind = itertools.cycle(line)
    chamber: list[str] = ["+-------+"]
    empty_wall = "|.......|"
    rocks: list[list[str]] = [
        ["####"],
        [".#.", "###", ".#."],
        ["..#", "..#", "###"],
        ["#", "#", "#", "#"],
        ["##", "##"],
    ]
    falling_rocks = enumerate(itertools.cycle(rocks), 1)

    rock: list[str] | None = None
    x: int = 0
    y: int = 0
    last_rock1 = 2023  # 2023 12
    while True:
        if rock is None:
            rock_number, rock = next(falling_rocks)
            if rock_number == last_rock1:
                break

            x = 3
            y = 1 + accommodate_new_rock(chamber, empty_wall, rock)
            assert fill_rock(chamber, rock, x, y, empty=False)
            # print_chamber(chamber)

        # Wind
        w = next(wind)
        assert fill_rock(chamber, rock, x, y, empty=True)
        pre_x = x
        if w == '>':
            x += 1
        elif w == '<':
            x -= 1
        if not fill_rock(chamber, rock, x, y, empty=False):
            x = pre_x
            assert fill_rock(chamber, rock, x, y, empty=False)
        # print_chamber(chamber)

        # Fall
        assert fill_rock(chamber, rock, x, y, empty=True)
        y += 1
        if not fill_rock(chamber, rock, x, y, empty=False):
            y -= 1
            assert fill_rock(chamber, rock, x, y, empty=False, final=True)
            # Next rock
            rock = None
        # print_chamber(chamber)

    print_chamber(chamber)
    empty = 1  # 1 is for down floor
    for c in reversed(chamber):
        if c == empty_wall:
            empty += 1
        else:
            break
    print(len(chamber) - empty)


if __name__ == "__main__":
    solution(utils.get_level())
