def count(pyramid: list, tuple_number: int):
    for i, number in enumerate(pyramid[tuple_number]):
        left = pyramid[tuple_number + 1][i] + number
        right = pyramid[tuple_number + 1][i + 1] + number
        pyramid[tuple_number][i] = max(left, right)
    return count(pyramid, tuple_number - 1) \
        if tuple_number - 1 >= 0 else pyramid[0][0]


def count_gold(pyramid: tuple):
    """
    Return max possible sum in a path from top to bottom
    """
    pyramid_list = [[pi for pi in p] for p in pyramid]
    pyramid_list.append([0] * (len(pyramid[-1]) + 1))
    max_value = count(pyramid_list, len(pyramid_list) - 2)
    return max_value


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert count_gold((
        (9,),
        (2, 2),
        (3, 3, 3),
        (4, 4, 4, 4)
    )) == 18, "Third example"
    assert count_gold((
        (1,),
        (2, 3),
        (3, 3, 1),
        (3, 1, 5, 4),
        (3, 1, 3, 1, 3),
        (2, 2, 2, 2, 2, 2),
        (5, 6, 4, 5, 6, 4, 3)
    )) == 23, "First example"
    assert count_gold((
        (1,),
        (2, 1),
        (1, 2, 1),
        (1, 2, 1, 1),
        (1, 2, 1, 1, 1),
        (1, 2, 1, 1, 1, 1),
        (1, 2, 1, 1, 1, 1, 9)
    )) == 15, "Second example"
    assert count_gold((
        (6,),
        (6, 9),
        (7, 1, 4),
        (6, 9, 9, 7),
        (1, 6, 7, 9, 7),
        (5, 7, 2, 6, 0, 9),
        (1, 2, 2, 6, 0, 1, 6),
        (8, 5, 0, 3, 1, 4, 3, 1),
        (9, 6, 4, 1, 1, 9, 3, 7, 9),
        (5, 8, 4, 3, 5, 4, 5, 1, 8, 3)
    )) == 66, 'Basic 8'
    assert count_gold((
        (4,),
        (4, 0),
        (3, 0, 9),
        (7, 5, 7, 1),
        (9, 1, 4, 1, 7),
        (5, 6, 5, 6, 5, 8),
        (3, 9, 9, 8, 3, 3, 7),
        (4, 7, 2, 6, 0, 6, 6, 7),
        (6, 6, 2, 9, 6, 1, 0, 2, 5),
        (9, 0, 7, 5, 3, 1, 4, 6, 0, 3)
    )) == 62, 'Extra 1'
    assert count_gold((
        (2,),
        (7, 7),
        (2, 5, 9),
        (0, 5, 8, 4),
        (3, 2, 1, 5, 2),
        (6, 4, 2, 6, 7, 2),
        (7, 5, 9, 4, 7, 6, 6),
        (1, 9, 4, 4, 5, 7, 3, 1),
        (9, 3, 1, 0, 0, 1, 1, 0, 9),
        (7, 6, 4, 8, 3, 6, 8, 7, 9, 0)
    )) == 61, 'Extra 2'
    assert count_gold((
        (3,),
        (7, 8),
        (4, 7, 3),
        (4, 7, 1, 6),
        (6, 3, 7, 1, 4),
        (3, 4, 8, 4, 4, 5),
        (3, 8, 1, 0, 1, 9, 6),
        (7, 1, 4, 1, 9, 8, 5, 5),
        (6, 4, 5, 8, 5, 3, 1, 0, 5)
    )) == 54, 'Extra 3'
    assert count_gold((
        (4,),
        (1, 7),
        (9, 9, 7),
        (4, 9, 9, 3),
        (3, 5, 3, 7, 5),
        (1, 7, 5, 3, 5, 6),
        (6, 5, 5, 8, 3, 3, 3),
        (6, 8, 6, 8, 7, 3, 7, 5),
        (7, 9, 9, 1, 6, 8, 7, 5, 9),
        (2, 8, 2, 5, 5, 5, 2, 5, 7, 8),
        (1, 3, 5, 2, 4, 5, 3, 5, 1, 1, 6),
        (8, 6, 1, 1, 3, 4, 7, 5, 3, 6, 1, 9),
        (5, 8, 6, 6, 2, 6, 9, 3, 7, 4, 6, 9, 9),
        (3, 3, 5, 4, 4, 6, 9, 2, 5, 7, 7, 1, 6, 7),
        (8, 1, 4, 4, 6, 8, 4, 9, 7, 6, 1, 8, 4, 2, 9),
        (6, 5, 8, 6, 8, 3, 2, 4, 8, 8, 1, 5, 6, 8, 8, 7),
        (6, 3, 9, 1, 5, 6, 7, 7, 2, 2, 6, 2, 2, 1, 8, 8, 6),
        (4, 7, 8, 7, 5, 2, 8, 8, 2, 2, 7, 1, 3, 8, 1, 9, 4, 7),
        (1, 7, 8, 1, 4, 3, 8, 6, 6, 9, 6, 3, 5, 4, 7, 6, 4, 5, 6),
        (1, 1, 4, 9, 9, 8, 3, 3, 8, 1, 8, 1, 7, 6, 6, 3, 2, 1, 1, 6)
    )) == 139, 'Extra 12'

    print('Ok!')
