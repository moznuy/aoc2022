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
    value: int | str

    def evaluate(self):
        if isinstance(self.value, str):
            raise ValueError("Unknown value")
        return self.value

    def __str__(self):
        return f"{self.value}"


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

    def __str__(self):
        return f"({self.left!s} {self.operation} {self.right!s})"


class Proxy:
    def __init__(self, wrappee: Node):
        self.wrappee = wrappee

    def __getattr__(self, attr):
        return getattr(self.wrappee, attr)

    def __str__(self):
        return str(self.wrappee)
        # return f"P {self.wrappee}"


def solve(root: Node, value: int | None = None) -> int:
    if isinstance(root, Value):
        assert value is not None
        return value

    known_value: int | None = 0
    unknown_expr: Node | None = None
    assert isinstance(root, Operation)
    for cur in (root.left, root.right):
        try:
            known_value = cur.evaluate()
        except ValueError:
            unknown_expr = cur.wrappee

    assert unknown_expr is not None
    assert known_value is not None

    if value is None:
        return solve(unknown_expr, known_value)
    if root.operation == '+':
        return solve(unknown_expr, value - known_value)
    if root.operation == '-':
        if root.left.wrappee is unknown_expr:
            return solve(unknown_expr, value + known_value)
        return solve(unknown_expr, known_value - value)
    if root.operation == '*':
        return solve(unknown_expr, value // known_value)
    if root.left.wrappee is unknown_expr:
        return solve(unknown_expr, value * known_value)
    return solve(unknown_expr, known_value // value)


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

    # Part 2
    root = tree['root']
    assert isinstance(root.wrappee, Operation)
    tree['humn'].wrappee = Value('humn', 'x')
    print(solve(root.wrappee))


def main(level: int):
    solution(level)


if __name__ == "__main__":
    main(utils.get_level())
