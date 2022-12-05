import re
from contextlib import suppress

import utils


def solution(level):
    reg = re.compile(r"move (?P<amount>\d+) from (?P<from>\d+) to (?P<to>\d+)")
    start = True
    vecs = ["" for _ in range(10)]

    for line in utils.input_reader(chars="\n"):
        if not line.strip():
            start = False
            for i, vec in enumerate(vecs):
                vecs[i] = vec[::-1]
            continue

        if start:
            for i in range(len(line) // 4 + 1):
                sub_line = line[i*4: (i+1)*4].strip()
                if not sub_line:
                    continue

                # for 1 2 3 4 line
                with suppress(IndexError):
                    vecs[i] += sub_line[1]
            continue

        match = reg.match(line)
        assert match
        amount = int(match['amount'])
        loc1 = int(match['from']) - 1
        loc2 = int(match['to']) - 1

        tmp = vecs[loc1][-amount:]
        vecs[loc1] = vecs[loc1][:-amount]
        if level == 1:
            tmp = tmp[::-1]
        vecs[loc2] += tmp

    for vec in vecs:
        if not vec:
            continue
        print(vec[-1], end='')
    print()


if __name__ == '__main__':
    solution(utils.get_level())
