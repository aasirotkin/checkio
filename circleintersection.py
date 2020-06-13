from typing import List, Tuple


def count_chains(circles: List[Tuple[int, int, int]]) -> int:
    length = len(circles)
    chains = [(i + 1) for i in range(length)]
    for i in range(length):
        x1, y1, r1 = circles[i]
        for j in range(i + 1, length):
            x2, y2, r2 = circles[j]
            d = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            if abs(r1 - r2) < d < (r1 + r2):
                min_chain = min(chains[i], chains[j])
                max_chain = max(chains[i], chains[j])
                for k in range(length):
                    if chains[k] == max_chain:
                        chains[k] = min_chain
    return len(set(chains))


if __name__ == '__main__':
    # These "asserts" are used for self-checking and not for an auto-testing
    assert count_chains([(1, 1, 1), (4, 2, 1), (4, 3, 1)]) == 2, 'basic'
    assert count_chains([(1, 1, 1), (2, 2, 1), (3, 3, 1)]) == 1, 'basic #2'
    assert count_chains([(2, 2, 2), (4, 2, 2), (3, 4, 2)]) == 1, 'trinity'
    assert count_chains([(2, 2, 1), (2, 2, 2)]) == 2, 'inclusion'
    assert count_chains([(1, 1, 1), (1, 3, 1), (3, 1, 1), (3, 3, 1)]) == 4, 'adjacent'
    assert count_chains([(0, 0, 1), (-1, 1, 1), (1, -1, 1), (-2, -2, 1)]) == 2, 'negative coordinates'
    assert count_chains([[0, 0, 2], [1, 0, 3], [3, 0, 1], [2, 1, 1], [-2, -2, 1], [0, 0, 4], [-3, 0, 1]]) == 3
    assert count_chains(
        [[-5, 0, 2], [-3, -2, 3], [-5, -6, 1], [10, -3, 4], [0, -9, 4], [9, 8, 2], [2, 2, 2], [5, -9, 4],
         [-1, -5, 1]]) == 4
    print("Coding complete? Click 'Check' to earn cool rewards!")
