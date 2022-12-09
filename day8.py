import utils


# TODO: Nope, just write N^2 for simplicity
def solution1():
    lines = [[int(digit) for digit in line] for line in utils.input_reader()]
    dims = len(lines), len(lines[0])
    shadow = []
    ans = [[False] * dims[1] for _ in range(dims[0])]

    def fill_shadow():
        nonlocal shadow
        shadow = [[0] * dims[1] for _ in range(dims[0])]

        for ii in range(dims[0]):
            shadow[ii][0] = lines[ii][0]
            shadow[ii][-1] = lines[ii][-1]
        for ii in range(dims[1]):
            shadow[0][ii] = lines[0][ii]
            shadow[-1][ii] = lines[-1][ii]

    for i in range(dims[0]):
        ans[i][0] = True
        ans[i][-1] = True
    for i in range(dims[1]):
        ans[0][i] = True
        ans[-1][i] = True

    # Down
    fill_shadow()
    for i in range(1, dims[0] - 1):
        for j in range(1, dims[1] - 1):
            if lines[i][j] > shadow[i - 1][j]:
                ans[i][j] = True
            shadow[i][j] = max(shadow[i - 1][j], lines[i][j])

    # Up
    fill_shadow()
    for i in range(dims[0] - 2, 0, -1):
        for j in range(1, dims[1] - 1):
            if lines[i][j] > shadow[i + 1][j]:
                ans[i][j] = True
            shadow[i][j] = max(shadow[i + 1][j], lines[i][j])

    # Right
    fill_shadow()
    for i in range(1, dims[1] - 1):
        for j in range(1, dims[0] - 1):
            if lines[j][i] > shadow[j][i - 1]:
                ans[j][i] = True
            shadow[j][i] = max(shadow[j][i - 1], lines[j][i])

    # Left
    fill_shadow()
    for i in range(dims[1] - 2, 0, -1):
        for j in range(1, dims[0] - 1):
            if lines[j][i] > shadow[j][i + 1]:
                ans[j][i] = True
            shadow[j][i] = max(shadow[j][i + 1], lines[j][i])

    print(sum(a for an in ans for a in an))


# Ahhhh, N^2 but so much more elegant!
def solution2():
    lines = [[int(digit) for digit in line] for line in utils.input_reader()]
    dims = len(lines), len(lines[0])

    max_saw = 0
    for y in range(1, dims[0] - 1):
        for x in range(1, dims[1] - 1):
            cur_saw = 1
            for vel in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                coord = y, x
                saw = 0
                while True:
                    coord = coord[0] + vel[0], coord[1] + vel[1]
                    if 0 <= coord[0] < dims[0] and 0 <= coord[1] < dims[1]:
                        saw += 1
                        if lines[y][x] <= lines[coord[0]][coord[1]]:
                            break
                    else:
                        break
                cur_saw *= saw
            max_saw = max(max_saw, cur_saw)
    print(max_saw)


if __name__ == '__main__':
    if utils.get_level() == 1:
        solution1()
    else:
        solution2()
