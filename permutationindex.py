from typing import Tuple, Iterable
from math import factorial

fac = lambda x: (x * fac(x - 1) if x > 1 else x) if x > 0 else 1
shift = lambda n, i: len([1 for j in range(0, i) if n[j] < n[i]])


def permutation_index(num: Tuple[int], i=0) -> int:
    l = len(num) - 1 - i
    index = (num[i] - shift(num, i)) * fac(l)
    return (index + permutation_index(num, i + 1)) \
        if l > 1 else (index + 1)


def reversed_permutation_index(length: int, index: int, rng=[]) -> Iterable[int]:
    rng = list(range(length))
    r = []
    for l in rng[::-1]:
        f = fac(l)
        ind = (index - 1) // f
        n = rng.pop(ind)
        index -= ind * f
        r.append(n)

    return r


def reversed_permutation_index2(length: int, index: int) -> Iterable[int]:
    fact = [factorial(n) for n in range(length - 1, -1, -1)]
    pool = [i for i in range(length)]
    nums = [pool.pop(((index - 1) // n) % len(pool)) for n in fact]
    return nums


if __name__ == '__main__':
    assert permutation_index((0, 1, 2)) == 1
    assert permutation_index((2, 1, 3, 0, 4, 5)) == 271
    assert permutation_index((6, 8, 3, 4, 2, 1, 7, 5, 0)) == 279780
    assert permutation_index((0, 4, 7, 5, 8, 2, 10, 6, 3, 1, 9, 11)) == 12843175
    assert permutation_index((9, 0, 6, 2, 5, 7, 12, 10, 3, 8, 11, 4, 13, 1, 14)) == 787051783737
    assert permutation_index((9, 0, 6, 17, 8, 12, 11, 1, 10, 14, 3, 15, 2, 13, 16, 7, 5, 4)) == 3208987196401056
    assert permutation_index(
        (15, 13, 14, 6, 10, 5, 19, 16, 11, 0, 9, 18, 2, 17, 4, 20, 12, 1, 3, 7, 8)) == 38160477453633042937
    assert permutation_index((9, 5, 4, 12, 13, 17, 7, 0, 23, 16, 11, 8, 15, 21, 2, 3, 22, 1, 10, 19, 6, 20, 14,
                              18)) == 238515587608877815254677
    assert permutation_index((16, 17, 10, 23, 4, 22, 7, 18, 2, 21, 13, 6, 9, 8, 19, 3, 25, 12, 26, 24, 14, 1, 0, 20, 15,
                              5, 11)) == 6707569694907742966546817183

    assert tuple(reversed_permutation_index(3, 5)) == (2, 0, 1)
    assert tuple(reversed_permutation_index(9, 279780)) == (6, 8, 3, 4, 2, 1, 7, 5, 0)
    assert tuple(reversed_permutation_index(6, 271)) == (2, 1, 3, 0, 4, 5)
    assert tuple(reversed_permutation_index(12, 12843175)) == (0, 4, 7, 5, 8, 2, 10, 6, 3, 1, 9, 11)
    assert tuple(reversed_permutation_index(15, 787051783737)) == (9, 0, 6, 2, 5, 7, 12, 10, 3, 8, 11, 4, 13, 1, 14)
    assert tuple(reversed_permutation_index(18, 3208987196401056)) == (
    9, 0, 6, 17, 8, 12, 11, 1, 10, 14, 3, 15, 2, 13, 16, 7, 5, 4)
    assert tuple(reversed_permutation_index(21, 38160477453633042937)) == (
    15, 13, 14, 6, 10, 5, 19, 16, 11, 0, 9, 18, 2, 17, 4, 20, 12, 1, 3, 7, 8)
    assert tuple(reversed_permutation_index(24, 238515587608877815254677)) == (
    9, 5, 4, 12, 13, 17, 7, 0, 23, 16, 11, 8, 15, 21, 2, 3, 22, 1, 10, 19, 6, 20, 14, 18)
    assert tuple(reversed_permutation_index(27, 6707569694907742966546817183)) == (
    16, 17, 10, 23, 4, 22, 7, 18, 2, 21, 13, 6, 9, 8, 19, 3, 25, 12, 26, 24, 14, 1, 0, 20, 15, 5, 11)

    print('The local tests are done. Click on "Check" for more real tests.')
