def solution(elves_count=1):
    cur_elf = 0
    max_elves = [0] * elves_count

    with open('input.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                max_elves = sorted(max_elves + [cur_elf], reverse=True)[:elves_count]
                cur_elf = 0
            else:
                cur_elf += int(line)

    print(sum(max_elves))


if __name__ == '__main__':
    solution()
    solution(3)
