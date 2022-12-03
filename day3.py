import utils


def solution1():
    s = 0

    for line in utils.input_reader():
        first = line[0: len(line)//2]
        second = line[len(line)//2:]
        inter = set(first).intersection(set(second))
        assert len(inter) == 1
        item: str = inter.pop()
        priority = ord(item) - ord('a') + 1 if item.islower() else ord(item) - ord('A') + 27
        # print(item, priority)
        s += priority
    print(s)


def solution2():
    s = 0
    sets = [set(), set(), set()]

    for i, line in enumerate(utils.input_reader()):
        sets[i % 3] = set(line)

        if i % 3 != 2:
            continue

        inter = sets[0].intersection(sets[1]).intersection(sets[2])
        assert len(inter) == 1
        item: str = inter.pop()
        priority = ord(item) - ord('a') + 1 if item.islower() else ord(item) - ord('A') + 27
        s += priority
    print(s)


if __name__ == '__main__':
    if utils.get_part() == 1:
        solution1()
    else:
        solution2()
