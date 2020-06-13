from itertools import product


def steps_to_convert(line1, line2):
    l1, l2 = len(line1), len(line2)
    m = [[0] * (l2 + 1) for l in range(l1 + 1)]
    for i in range(1, l1 + 1): m[i][0] = i
    for i in range(1, l2 + 1): m[0][i] = i

    for i, j in product(range(1, l1 + 1), range(1, l2 + 1)):
        cost = 1 if line1[i - 1] != line2[j - 1] else 0
        m[i][j] = min(m[i - 1][j - 1] + cost,
                      m[i - 1][j] + 1,
                      m[i][j - 1] + 1)

    return m[l1][l2]


if __name__ == "__main__":
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert steps_to_convert('line1', 'line1') == 0, "eq"
    assert steps_to_convert('line1', 'line2') == 1, "2"
    assert steps_to_convert('line', 'line2') == 1, "none to 2"
    assert steps_to_convert('ine', 'line2') == 2, "need two more"
    assert steps_to_convert('line1', '1enil') == 4, "everything is opposite"
    assert steps_to_convert('', '') == 0, "two empty"
    assert steps_to_convert('l', '') == 1, "one side"
    assert steps_to_convert('', 'l') == 1, "another side"
    print("You are good to go!")
