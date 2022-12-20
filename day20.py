import dataclasses
import operator

import utils


SEQ = 0


def factory():
    global SEQ
    SEQ += 1
    return SEQ


@dataclasses.dataclass(frozen=True, eq=True)
class Number:
    number: int
    nonce: int = dataclasses.field(default_factory=factory)


def print_sequence(input_sequence: list[Number], numbers: dict[int, Number]):
    print(" ".join(str(numbers[i].number) for i in range(len(input_sequence))))


def solution(level):
    multiplier = 1 if level == 1 else 811589153
    input_sequence: list[Number] = [
        Number(int(line) * multiplier) for line in utils.input_reader()
    ]
    indices: dict[Number, int] = {
        number: index for index, number in enumerate(input_sequence)
    }
    numbers: dict[int, Number] = {
        index: number for index, number in enumerate(input_sequence)
    }
    check_zero: list[Number] = list(
        map(
            operator.itemgetter(0),
            filter(lambda ind: ind[0].number == 0, indices.items()),
        )
    )
    assert len(check_zero) == 1
    zero_number: Number = check_zero[0]

    modulos = len(input_sequence)
    # print_sequence(input_sequence, numbers)

    rounds = 1 if level == 1 else 10
    for _round in range(rounds):
        print(_round)
        for n in input_sequence:
            # print(step / modulos * 100)
            index = indices[n]
            vel = n.number // abs(n.number) if n.number else 0
            move_by = abs(n.number) % (modulos - 1)
            # if move_by > modulos // 2:
            #     vel *= -1
            #     move_by = modulos - move_by - 1

            for i in range(move_by):
                new_index = (index + vel) % modulos
                new_number = numbers[new_index]

                indices[new_number] = index
                indices[n] = new_index
                numbers[new_index] = n
                numbers[index] = new_number

                index = new_index
            # print_sequence(input_sequence, numbers)
        # print_sequence(input_sequence, numbers)
    # print_sequence(input_sequence, numbers)
    ans = 0
    for plus in (1000, 2000, 3000):
        index = (indices[zero_number] + plus) % modulos
        number = numbers[index].number
        # print(number)
        ans += number
    print(ans)


def main(level: int):
    solution(level)


if __name__ == "__main__":
    main(1)
