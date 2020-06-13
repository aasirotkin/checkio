from itertools import product


def find_chain(matrix, matr_map, p, q, matr_len, n):
    c = 0
    # right
    if q != (matr_len - 1) \
            and matr_map[p][q + 1] == -1 \
            and matrix[p][q + 1] == n:
        matr_map[p][q + 1] = n
        c += 1 + find_chain(matrix, matr_map, p, q + 1, matr_len, n)
    # down
    if p != (matr_len - 1) \
            and matr_map[p + 1][q] == -1 \
            and matrix[p + 1][q] == n:
        matr_map[p + 1][q] = n
        c += 1 + find_chain(matrix, matr_map, p + 1, q, matr_len, n)
    # left
    if q != 0 \
            and matr_map[p][q - 1] == -1 \
            and matrix[p][q - 1] == n:
        matr_map[p][q - 1] = n
        c += 1 + find_chain(matrix, matr_map, p, q - 1, matr_len, n)
    # up
    if p != 0 \
            and matr_map[p - 1][q] == -1 \
            and matrix[p - 1][q] == n:
        matr_map[p - 1][q] = n
        c += 1 + find_chain(matrix, matr_map, p - 1, q, matr_len, n)

    return c


def next_chain(matrix, matr_map, prl):
    n, p, q = -1, -1, -1
    for i, j in prl:
        if matr_map[i][j] == -1:
            p, q = i, j
            n = matrix[p][q]
            break
    return n, p, q


def checkio(matrix):
    matr_len = len(matrix)
    matr_map = [[-1] * matr_len for i in range(matr_len)]
    prl = product(range(matr_len), range(matr_len))
    res = [0, 0]
    while True:
        n, p, q = next_chain(matrix, matr_map, prl)
        if n == -1:
            break
        matr_map[p][q] = n
        c = 1 + find_chain(matrix, matr_map, p, q, matr_len, n)
        if res[0] < c:
            res[0], res[1] = c, n
    return res


# These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio([
        [1, 2, 3, 4, 5],
        [1, 1, 1, 2, 3],
        [1, 1, 1, 2, 2],
        [1, 2, 2, 2, 1],
        [1, 1, 1, 1, 1]
    ]) == [14, 1], "14 of 1"

    assert checkio([
        [2, 1, 2, 2, 2, 4],
        [2, 5, 2, 2, 2, 2],
        [2, 5, 4, 2, 2, 2],
        [2, 5, 2, 2, 4, 2],
        [2, 4, 2, 2, 2, 2],
        [2, 2, 4, 4, 2, 2]
    ]) == [19, 2], '19 of 2'

    assert checkio([
        [5, 1, 5],
        [5, 5, 5],
        [5, 3, 2]
    ]) == [6, 5]

    assert checkio([
        [1, 1, 5, 1, 1, 4, 2],
        [2, 4, 3, 2, 3, 4, 5],
        [1, 5, 4, 4, 4, 1, 1],
        [1, 4, 4, 2, 5, 1, 3],
        [4, 4, 1, 1, 1, 5, 3],
        [4, 2, 1, 3, 5, 3, 3],
        [4, 5, 2, 1, 4, 5, 5]
    ]) == [9, 4]
