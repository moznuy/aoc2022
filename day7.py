import dataclasses
import re
from collections.abc import MutableMapping
from typing import List
from typing import Optional

import utils


@dataclasses.dataclass(kw_only=True)
class File:
    name: str
    size: int


@dataclasses.dataclass(kw_only=True)
class Directory:
    name: str
    _total_size: Optional[int] = None
    directories: MutableMapping["str", "Directory"] = dataclasses.field(
        default_factory=dict
    )
    files: MutableMapping["str", File] = dataclasses.field(default_factory=dict)
    parent: "Directory" = None

    @property
    def total_size(self):
        if self._total_size is not None:
            return self._total_size

        self._total_size = 0
        self._total_size += sum(
            directory.total_size for directory in self.directories.values()
        )
        self._total_size += sum(file.size for file in self.files.values())
        return self._total_size


def solution(level):
    reg = re.compile(r"^(?P<size>\d+) (?P<name>.+)$")
    root = Directory(name="/")
    cur: Optional[Directory] = None
    ls_mod = False

    for line in utils.input_reader():
        if ls_mod:
            if line.startswith("$"):
                ls_mod = False
            elif line.startswith("dir"):
                name = line.split()[-1]
                assert name
                assert cur
                cur.directories[name] = Directory(name=name, parent=cur)
                continue
            else:
                match = reg.match(line)
                assert match
                assert cur
                cur.files[match["name"]] = File(
                    name=match["name"], size=int(match["size"])
                )
                continue

        if line.startswith("$ ls"):
            ls_mod = True
            continue

        if line.startswith("$ cd"):
            where = line.split()[-1]

            if where == "/":
                cur = root
                continue
            if where == "..":
                assert cur
                cur = cur.parent
                continue
            cur = cur.directories[where]
            continue
        assert False

    # print(root.total_size)

    if level == 1:

        def sol(pos: Directory):
            answer = 0
            if pos.total_size <= 100000:
                answer += pos.total_size

            answer += sum(sol(directory) for directory in pos.directories.values())
            return answer

        print(sol(root))
    else:

        def collect(pos: Directory) -> List[int]:
            answer: List[int] = [pos.total_size]
            answer.extend(
                item
                for directory in pos.directories.values()
                for item in collect(directory)
            )
            return answer

        free_space = 70000000 - root.total_size
        sorted_collect = sorted(collect(root))
        ans = next(item for item in sorted_collect if free_space + item >= 30000000)
        print(ans)


if __name__ == "__main__":
    solution(utils.get_level())
