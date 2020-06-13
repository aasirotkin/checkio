def checkio(stair_values):
    """Return the best score when traveling up stairs scored by stair_values."""
    # Use dynamic programming to solve this in linear time.
    # Pad initial list to eliminate edge cases.
    values = [0] + stair_values + [0]
    for i in range(1, len(values)):
        values[i] += max(values[i - 1], values[i - 2])
    return values[-1]


# These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio([5, -3, -1, 2]) == 6, 'Fifth'
    assert checkio([5, 6, -10, -7, 4]) == 8, 'First'
    assert checkio([-11, 69, 77, -51, 23, 67, 35, 27, -25, 95]) == 393, 'Second'
    assert checkio([-21, -23, -69, -67, 1, 41, 97, 49, 27]) == 125, 'Third'
    print('All ok')
