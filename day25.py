import itertools

import utils


def plus(a: list[int], b: list[int]) -> list[int]:
    ans = [0 for _ in range(max(len(a), len(b)) + 2)]
    for i, (d1, d2) in enumerate(itertools.zip_longest(a, b, fillvalue=0)):
        ans[i] += d1 + d2
        if ans[i] < -2:
            ans[i + 1] -= 1
            ans[i] += 5
        if ans[i] > 2:
            ans[i + 1] += 1
            ans[i] -= 5
    while ans[-1] == 0:
        ans.pop()
    return ans


def solution(level: int) -> None:
    mapper = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
    inv_mapper = {v: k for k, v in mapper.items()}

    numbers = [
        list(reversed([mapper[s] for s in line])) for line in utils.input_reader()
    ]
    ans = [0]
    for number in numbers:
        ans = plus(ans, number)
    ans = list(reversed(ans))
    print(ans)
    for digit in ans:
        print(inv_mapper[digit], end="")
    print()


def main(level: int) -> None:
    solution(level)


if __name__ == "__main__":
    main(utils.get_level())
