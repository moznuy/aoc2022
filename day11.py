import dataclasses
import enum
from operator import attrgetter
from typing import Generator
from typing import List

import utils


class Operation(enum.Enum):
    Plus = enum.auto()
    Multiplication = enum.auto()


@dataclasses.dataclass()
class Monkey:
    number: int
    items: List[int]
    operation: Operation
    operation_number: int
    test: int
    test_true: int
    test_false: int
    inspected: int = 0


def monkey_generator(inp: Generator[str, None, None]) -> Generator[Monkey, None, None]:
    while True:
        try:
            number = int(next(inp).split()[-1][:-1])
            items = list(map(int, next(inp).split(':')[-1].split(',')))
            operations = next(inp).split()[-2:]
            operation = Operation.Plus if operations[0] == '+' else Operation.Multiplication
            operation_number = -1 if operations[1] == 'old' else int(operations[1])
            test = int(next(inp).split()[-1])
            test_true = int(next(inp).split()[-1])
            test_false = int(next(inp).split()[-1])
            yield Monkey(number, items, operation, operation_number, test, test_true, test_false)
        except StopIteration:
            break


def solution(level: int):
    monkeys = [monkey for monkey in monkey_generator(utils.input_reader(empty_string=False))]
    modulus = 1
    for monkey in monkeys:
        modulus *= monkey.test

    for _round in range(1, 21 if level == 1 else 10001):
        for monkey in monkeys:
            if not monkey.items:
                continue

            for item in monkey.items:
                op = (lambda x, y: x + y) if monkey.operation == Operation.Plus else (lambda x, y: x * y)
                worry = op(item, monkey.operation_number if monkey.operation_number >= 0 else item)
                if level == 1:
                    worry //= 3
                else:
                    worry %= modulus
                new_item = worry
                if worry % monkey.test == 0:
                    assert monkey.test_true != monkey.number
                    monkeys[monkey.test_true].items.append(new_item)
                else:
                    assert monkey.test_false != monkey.number
                    monkeys[monkey.test_false].items.append(new_item)
                monkey.inspected += 1
            monkey.items = []

        # if _round % 1000 == 0 or _round == 1 or _round == 20:
        #     print(_round)
        #     pprint.pprint(monkeys)

    active_monkeys = sorted(monkeys, key=attrgetter('inspected'), reverse=True)
    print(active_monkeys[0].inspected * active_monkeys[1].inspected)


if __name__ == "__main__":
    solution(utils.get_level())
