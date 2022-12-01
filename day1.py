def part1():
    cur_elf = 0
    max_elf = 0

    with open('input.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                max_elf = max(max_elf, cur_elf)
                cur_elf = 0
            else:
                cur_elf += int(line)

    print(max_elf)


def part2():
    cur_elf = 0
    max_elves = [0, 0, 0]

    with open('input.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                max_elves = sorted(max_elves + [cur_elf], reverse=True)[:3]
                # max_elf = max(max_elf, cur_elf)
                cur_elf = 0
            else:
                cur_elf += int(line)

    print(sum(max_elves))


if __name__ == '__main__':
    part1()
    part2()
