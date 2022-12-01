import utils


def solution(elves_count=1):
    cur_elf = 0
    max_elves = [0] * elves_count

    for line in utils.input_reader():
        if line:
            cur_elf += int(line)
        else:
            max_elves = sorted(max_elves + [cur_elf], reverse=True)[:elves_count]
            cur_elf = 0

    print(sum(max_elves))


if __name__ == '__main__':
    solution()
    solution(3)
