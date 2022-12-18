import re

import utils


def inside_second(b1, e1, b2, e2):
    return b2 <= b1 <= e2 and b2 <= e1 <= e2


def overlap(b1, e1, b2, e2):
    return b2 <= b1 <= e2 or b2 <= e1 <= e2


def solution(level):
    ans = 0
    reg = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")
    for line in utils.input_reader():
        match = reg.match(line)
        assert match, line
        b1, e1, b2, e2 = (int(match[i]) for i in range(1, 5))

        f = inside_second if level == 1 else overlap
        if f(b1, e1, b2, e2) or f(b2, e2, b1, e1):
            ans += 1
    print(ans)


if __name__ == "__main__":
    solution(utils.get_level())
