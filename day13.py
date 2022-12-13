from __future__ import annotations

from functools import cmp_to_key
from itertools import zip_longest
from typing import Iterable

import utils


def pair_input() -> Iterable[tuple[list, list]]:
    gen = utils.input_reader(empty_string=False)
    while True:
        try:
            ldict = {}
            # TODO: Do smth not so simple )
            for s in ("l1", "l2"):
                _s = f"{s} = {next(gen)}"
                exec(_s, globals(), ldict)
            yield ldict["l1"], ldict["l2"]
        except StopIteration:
            break


def compare(l1: list | int, l2: list | int) -> bool | None:
    if isinstance(l1, int) and isinstance(l2, int):
        if l1 == l2:
            return None
        return l1 < l2

    if isinstance(l1, list) and isinstance(l2, list):
        for v1, v2 in zip_longest(l1, l2):
            if v1 is None:
                return True
            if v2 is None:
                return False
            res = compare(v1, v2)
            if res is not None:
                return res
        return None

    if isinstance(l1, int):
        return compare([l1], l2)

    if isinstance(l2, int):
        return compare(l1, [l2])

    assert False


def solution1():
    ans = 0
    for i, (l1, l2) in enumerate(pair_input(), 1):
        if compare(l1, l2):
            ans += i
    print(ans)


def solution2():
    _packets = [pair for pair in pair_input()]
    packets = [item for sublist in _packets for item in sublist]
    packets.append([[2]])
    packets.append([[6]])

    def cmp(l1, l2):
        res = compare(l1, l2)
        if res is None:
            return 0
        if res:
            return -1
        return 1

    packets = sorted(packets, key=cmp_to_key(cmp))
    i1 = packets.index([[2]]) + 1
    i2 = packets.index([[6]]) + 1
    print(i1 * i2)


if __name__ == "__main__":
    if utils.get_level() == 1:
        solution1()
    else:
        solution2()
