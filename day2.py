import utils


def common(part):
    score = 0
    for line in utils.input_reader():
        a, b = line.split()
        condition = me = ord(b[0]) - (ord("X") - ord("A")) - ord("A")
        opponent = ord(a[0]) - ord("A")

        if part == 1:
            score += solution1(opponent, me)
        else:
            score += solution2(opponent, condition)

    print(score)


def solution1(opponent: int, me: int):
    round_score = 0

    if opponent == me:
        round_score += 3
    elif (opponent + 1) % 3 == me:
        round_score += 6
    round_score += me + 1

    return round_score


def solution2(opponent: int, condition: int):
    round_score = 0

    if condition == 1:
        round_score += 3 + (opponent + 1)
    elif condition == 0:
        round_score += 0 + ((opponent - 1) % 3) + 1
    else:
        round_score += 6 + ((opponent + 1) % 3) + 1
    return round_score


if __name__ == "__main__":
    common(utils.get_level())
