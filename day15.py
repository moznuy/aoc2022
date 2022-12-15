from __future__ import annotations

import re

import utils


def part1(corners, circles, nope, y=10):
    ans = 0
    for x in range(corners[0], corners[2] + 1):
        for circle in circles:
            if (x, y) not in nope and abs(circle[0] - x) + abs(circle[1] - y) <= circle[
                2
            ]:
                ans += 1
                break
    return ans


def combine_segment(
    s: tuple[int, int], t: tuple[int, int]
) -> tuple[bool, tuple[int, int] | None]:
    if s[0] <= t[0] <= s[1]:
        if s[0] <= t[1] <= s[1]:
            return True, s
        return True, (s[0], t[1])
    return False, None


def part1better(
    circles: list[tuple[int, int, int]], y: int = 10
) -> list[tuple[int, int]]:
    segments: list[tuple[int, int]] = []
    # circle = (8, 7, 9)
    for circle in circles:
        r = circle[2]
        h = abs(circle[1] - y)
        # print(y, max(, 0))
        if 2 * (r - h) + 1 > 0:
            segments.append((circle[0] - (r - h), circle[0] + (r - h)))
    # break
    segments.sort()
    if not segments:
        return []

    ans = [segments[0]]
    for segment in segments:
        s1 = ans[-1]
        success, seg = combine_segment(s1, segment)
        if success:
            ans[-1] = seg
        else:
            ans.append(segment)

    return ans


def solution(level):
    reg = re.compile(r"=([-\d]+)")
    corners: list[int] = [10**20, 10**20, -(10**20), -(10**20)]
    circles: list[tuple[int, int, int]] = []
    nope: set[tuple[int, int]] = set()

    for line in utils.input_reader():
        x, y, x2, y2 = map(int, (match for match in reg.findall(line)))
        r = abs(x2 - x) + abs(y2 - y)
        circles.append((x, y, r))
        nope.add((x, y))
        nope.add((x2, y2))
        corners[0] = min(corners[0], x, x2, x - r)
        corners[1] = min(corners[1], y, y2, y - r)
        corners[2] = max(corners[2], x, x2, x + r)
        corners[3] = max(corners[3], y, y2, y + r)

    if level == 1:
        question = 2000000  # 10
        segments = part1better(circles, y=question)  # 2000000
        assert len(segments) == 1
        segment = segments[0]
        mn = 0
        for n in nope:
            if n[1] == question and segment[0] <= n[0] <= segment[1]:
                mn += 1
        print(segment[1] - segment[0] + 1 - mn)
        return

    mx = 4000000  # 20
    for y in range(0, mx + 1):
        # print(y)
        # Nope, too slow....
        # for x in range(0, mx + 1):
        #     for circle in circles:
        #         if abs(circle[0] - x) + abs(circle[1] - y) <= circle[2]:
        #             break
        #     else:
        #         print(x, y)
        segments = part1better(circles, y=y)
        if len(segments) == 1:
            continue
        assert len(segments) == 2
        s1, s2 = segments
        assert s1[1] + 2 == s2[0]
        x = s1[1] + 1
        print(x * 4000000 + y)


if __name__ == "__main__":
    solution(utils.get_level())
