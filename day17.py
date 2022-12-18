import collections
import hashlib
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


# Investigation
# def string_to_int(s):
#     return int.from_bytes(hashlib.sha1(s.encode()).digest(), byteorder="little")
#
#
# def print_chamber(chamber: list[str]):
#     for i, c in enumerate(reversed(chamber)):
#         print(len(chamber) - i, string_to_int(c) % 1000)
#     print()


def find_repeat_last_non_empty_n(
        encounter: dict[tuple[str, ...], tuple[int, int]],
        chamber: list[str],
        empty_wall: str,
        rock_number: int,
        n: int
) -> tuple[int, int, int] | None:
    first_non_empty_wall = 0
    for c in reversed(chamber):
        if c == empty_wall:
            first_non_empty_wall += 1
        else:
            break

    if len(chamber) - first_non_empty_wall <= n:
        return None

    height = len(chamber) - first_non_empty_wall - 1  # 1 for floor
    window = tuple(chamber[-1 - first_non_empty_wall: -1 - first_non_empty_wall - n: -1])
    if window in encounter:
        previous_rock_number, previous_height = encounter[window]
        return height, rock_number - previous_rock_number, height - previous_height

    encounter[window] = rock_number, height
    return None


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
    encounter: dict[tuple[str, ...], tuple[int, int]] = {}

    rock: list[str] | None = None
    x: int = 0
    y: int = 0
    last_rock = 2022 if level == 1 else 1000000000000
    rock_number: int = 0
    # real_height = 0
    sim_height = 0

    remaining_rounds: int | None = None
    while True:
        if rock is None:
            if remaining_rounds is None:
                found = find_repeat_last_non_empty_n(encounter, chamber, empty_wall, rock_number, 50)
                if found is not None:
                    cur_height, rock_diff, height_difference = found
                    remaining_rocks = last_rock - rock_number
                    sim_rounds = remaining_rocks // rock_diff
                    remaining_rounds = remaining_rocks % rock_diff
                    # real_height = cur_height
                    sim_height = height_difference * sim_rounds
            else:
                remaining_rounds -= 1
                if remaining_rounds == 0:
                    break

            rock_number, rock = next(falling_rocks)

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

        # Fall
        assert fill_rock(chamber, rock, x, y, empty=True)
        y += 1
        if not fill_rock(chamber, rock, x, y, empty=False):
            y -= 1
            assert fill_rock(chamber, rock, x, y, empty=False, final=True)
            # Next rock
            rock = None

    found = find_repeat_last_non_empty_n(encounter, chamber, empty_wall, rock_number, 50)
    assert found
    cur_height = found[0]
    # cur_height - real_height
    # ans = real_height + sim_height + cur_height - real_height
    ans = sim_height + cur_height
    print(ans)


if __name__ == "__main__":
    solution(utils.get_level())
