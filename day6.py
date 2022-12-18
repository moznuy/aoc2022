import collections

import utils

from itertools import islice


# Python docs :)
def sliding_window(iterable, n):
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def solution(level):
    group = 4 if level == 1 else 14

    for line in utils.input_reader():
        for i, window in enumerate(sliding_window(line, group)):
            if len(set(window)) == group:
                print(i + group)
                break
        else:
            raise NotImplementedError


if __name__ == "__main__":
    solution(utils.get_level())
