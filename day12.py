import queue
from typing import List
from typing import MutableMapping
from typing import Optional
from typing import Tuple

import utils


def solution(level: int):
    grid: List[List[int]] = []
    start_x = start_y = end_x = end_y = None  # type: Optional[int]
    for y, line in enumerate(utils.input_reader()):
        grid.append([])
        for x, symbol in enumerate(line):
            if symbol.islower():
                grid[-1].append(ord(symbol) - ord("a"))
                continue
            if symbol == "S":
                grid[-1].append(0)
                start_x = x
                start_y = y
                continue
            if symbol == "E":
                grid[-1].append(ord("z") - ord("a"))
                end_x = x
                end_y = y
                continue
            assert False
    for var in (start_x, start_y, end_x, end_y):
        assert var is not None
    path: List[List[Optional[Tuple[int, int]]]] = [
        [None for _ in range(len(grid[0]))] for _ in range(len(grid))
    ]

    q: queue.Queue[Tuple[int, int]] = queue.Queue()
    start = (end_y, end_x)
    visited: MutableMapping[Tuple[int, int], int] = {start: 0}
    q.put(start)
    ans: Optional[int] = None

    while not q.empty():
        coord = q.get()
        cur_ans = visited[coord]
        height = grid[coord[0]][coord[1]]
        if coord == (start_y, start_x):
            ans = cur_ans
            break
        if level == 2 and height == 0:
            ans = cur_ans
            break

        for vel in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            try_coord = coord[0] + vel[0], coord[1] + vel[1]
            if (
                try_coord[0] < 0
                or try_coord[1] < 0
                or try_coord[0] >= len(grid)
                or try_coord[1] >= len(grid[0])
            ):
                continue
            try_height = grid[try_coord[0]][try_coord[1]]
            if not (
                try_height == height or try_height + 1 == height or try_height > height
            ):
                continue
            if try_coord in visited:
                continue
            path[try_coord[0]][try_coord[1]] = coord
            visited[try_coord] = cur_ans + 1
            q.put(try_coord)

    mapping = {
        (1, 0): "v",
        (0, 1): ">",
        (-1, 0): "^",
        (0, -1): "<",
    }
    for y in range(len(path)):
        for x in range(len(path[y])):
            if path[y][x] is None:
                print(".", end="")
                continue
            vel = path[y][x][0] - y, path[y][x][1] - x
            print(f"{mapping[vel]}", end="")
        print()
    print(ans)


if __name__ == "__main__":
    solution(utils.get_level())
