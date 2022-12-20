import utils


def solution(level: int):
    for line in utils.input_reader():
        print(line)


def main(level: int):
    solution(level)


if __name__ == "__main__":
    main(utils.get_level())
