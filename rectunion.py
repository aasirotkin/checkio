from typing import List, Tuple


def inside(row: int, col: int, rec: Tuple[int]) -> bool:
    return row >= rec[0] and col >= rec[1] and (row + 1) <= rec[2] and (col + 1) <= rec[3]


def rectangles_union(recs: List[Tuple[int]]) -> int:
    if not recs:
        return 0
    x_min = min(recs, key=lambda x: x[0])[0]
    y_min = min(recs, key=lambda x: x[1])[1]
    x_max = max(recs, key=lambda x: x[2])[2]
    y_max = max(recs, key=lambda x: x[3])[3]
    area = 0

    for row in range(x_min, x_max):
        for col in range(y_min, y_max):
            for rec in recs:
                if inside(row, col, rec):
                    area += 1
                    break

    return area


if __name__ == '__main__':
    print("Example:")
    print(rectangles_union([
        (6, 3, 8, 10),
        (4, 8, 11, 10),
        (16, 8, 19, 11)
    ]))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert rectangles_union([
        (6, 3, 8, 10),
        (4, 8, 11, 10),
        (16, 8, 19, 11)
    ]) == 33
    assert rectangles_union([
        (16, 8, 19, 11)
    ]) == 9
    assert rectangles_union([
        (16, 8, 19, 11),
        (16, 8, 19, 11)
    ]) == 9
    assert rectangles_union([
        (16, 8, 16, 8)
    ]) == 0
    assert rectangles_union([

    ]) == 0
    print("Coding complete? Click 'Check' to earn cool rewards!")
