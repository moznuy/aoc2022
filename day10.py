import dataclasses
from typing import Any
from typing import cast
from typing import Mapping
from typing import MutableMapping
from typing import Optional
from typing import Type

import utils


@dataclasses.dataclass
class Instruction:
    name: str
    cycles: int
    operand: Any = None

    def __init_subclass__(cls, **kwargs):
        cast(MutableMapping, instruction_map)[cls.name] = cls

    def work(self, register):
        raise NotImplementedError


instruction_map: Mapping[str, Type[Instruction]] = {}


@dataclasses.dataclass
class Noop(Instruction):
    name: str = 'noop'
    cycles: int = 1

    def work(self, register):
        return register


@dataclasses.dataclass
class Addx(Instruction):
    name: str = 'addx'
    cycles: int = 2
    operand: int = 0

    def work(self, register):
        return register + self.operand


def solution(level: int):
    cur: Optional[Instruction] = None
    cycle = 0
    register_x = 1
    next_check = 20
    signal_sum = 0

    crt_line = 0
    crt_index = 0

    op_generator = utils.input_reader()
    while True:
        cycle += 1
        if cur is None:
            try:
                line = next(op_generator)
            except StopIteration:
                break
            step = line.split()
            instruction = step[0]
            operand = int(step[1]) if len(step) > 1 else None
            cur = instruction_map[instruction](name=instruction, operand=operand)

        if cycle == next_check:
            signal = cycle * register_x
            signal_sum += signal
            next_check += 40

        if register_x - 1 <= crt_index <= register_x + 1:
            print('#', end='')
        else:
            print('.', end='')
        crt_index += 1
        if crt_index == 40:
            crt_index = 0
            crt_line += 1
            print()

        cur.cycles -= 1
        if cur.cycles == 0:
            register_x = cur.work(register_x)
            cur = None

    print()
    print(signal_sum)



if __name__ == "__main__":
    solution(utils.get_level())
