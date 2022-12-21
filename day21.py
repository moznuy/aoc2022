from __future__ import annotations

import dataclasses
import re

import utils


@dataclasses.dataclass(frozen=True, eq=True)
class Node:
    name: str

    def evaluate(self):
        raise NotImplementedError


@dataclasses.dataclass(frozen=True, eq=True)
class Value(Node):
    value: int

    def evaluate(self):
        return self.value


@dataclasses.dataclass(frozen=True, eq=True)
class Deffered(Node):
    pass


@dataclasses.dataclass(frozen=True, eq=True)
class Operation(Node):
    operation: str
    left: Proxy
    right: Proxy

    def evaluate(self):
        assert self.operation in {"+", "-", "*", "/"}
        if self.operation == "+":
            return self.left.evaluate() + self.right.evaluate()
        if self.operation == "-":
            return self.left.evaluate() - self.right.evaluate()
        if self.operation == "*":
            return self.left.evaluate() * self.right.evaluate()
        return self.left.evaluate() // self.right.evaluate()


class Proxy:
    def __init__(self, wrappee: Node):
        self.wrappee = wrappee

    def __getattr__(self, attr):
        return getattr(self.wrappee, attr)

    def __str__(self):
        return f"P {self.wrappee}"


def solution(level: int):
    tree: dict[str, Proxy[Node]] = {}

    for line in utils.input_reader():
        parent: str
        action: str
        parent, action = line.split(": ")

        cur = tree.setdefault(parent, Proxy(Deffered(name=parent)))

        try:
            value = int(action)
            cur.wrappee = Value(name=parent, value=value)
        except ValueError:
            match = re.fullmatch(
                r"(?P<left>\w+) (?P<operation>\W) (?P<right>\w+)", action
            )
            assert match
            left = tree.setdefault(match["left"], Proxy(Deffered(name=match["left"])))
            right = tree.setdefault(
                match["right"], Proxy(Deffered(name=match["right"]))
            )
            cur.wrappee = Operation(
                name=parent, operation=match["operation"], left=left, right=right
            )

    print(tree["root"].evaluate())


def main(level: int):
    solution(level)


if __name__ == "__main__":
    main(utils.get_level())
