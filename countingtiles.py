def checkio(radius, a=0, b=0):
    for x, y in __import__('itertools').product(range(-4, 4), range(-4, 4)):
        s = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
        c = [1 for x, y in s if abs(x + y * 1j) < radius]
        a, b = a + (sum(c) == 4), b + (0 < sum(c) < 4)
    return a, b


def checkio_my(radius, a=0, b=0):
    rng = round(radius) + 1
    for x, y in __import__('itertools').product(range(rng), range(rng)):
        s = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
        c = [1 for x, y in s if abs(x + y * 1j) < radius]
        a, b = a + 1 if sum(c) == 4 else a, b + 1 if 0 < sum(c) < 4 else b
    return [4 * a, 4 * b]


assert checkio_my(2) == [4, 12]
assert checkio_my(3) == [16, 20]
assert checkio_my(2.1) == [4, 20]
assert checkio_my(2.5) == [12, 20]
assert checkio_my(2.2) == [4, 20]

print('All right')
