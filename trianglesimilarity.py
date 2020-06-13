from typing import List, Tuple
Coords = List[Tuple[int, int]]


def module(x: int, y: int) -> int:
    return (x**2+y**2)**0.5


def vector(c1: Tuple, c2: Tuple) -> Tuple:
    x = c2[0]-c1[0]
    y = c2[1]-c1[1]
    r = module(x, y)
    return x, y, r


def cosine(v1: Tuple, v2: Tuple) -> int:
    return round(abs(v1[0]*v2[0] + v1[1]*v2[1])/(v1[2]*v2[2]), 10)


def angles(coord: Coords) -> Tuple:
    length = len(coord)
    v = [vector(coord[c1], coord[c2]) for c1 in range(length) for c2 in range(c1+1, length)]
    return tuple(cosine(v[c1], v[c2]) for c1 in range(length) for c2 in range(c1+1, length))


def similar_triangles(coords_1: Coords, coords_2: Coords) -> bool:
    a1 = angles(coords_1)
    a2 = angles(coords_2)
    return all(a in a2 for a in a1)


if __name__ == '__main__':
    print("Example:")
    print(similar_triangles([(0, 0), (1, 2), (2, 0)], [(3, 0), (4, 2), (5, 0)]))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert similar_triangles([(0, 0), (1, 2), (2, 0)], [(3, 0), (4, 2), (5, 0)]) is True, 'basic'
    assert similar_triangles([(0, 0), (1, 2), (2, 0)], [(3, 0), (4, 3), (5, 0)]) is False, 'different #1'
    assert similar_triangles([(0, 0), (1, 2), (2, 0)], [(2, 0), (4, 4), (6, 0)]) is True, 'scaling'
    assert similar_triangles([(0, 0), (0, 3), (2, 0)], [(3, 0), (5, 3), (5, 0)]) is True, 'reflection'
    assert similar_triangles([(1, 0), (1, 2), (2, 0)], [(3, 0), (5, 4), (5, 0)]) is True, 'scaling and reflection'
    assert similar_triangles([(1, 0), (1, 3), (2, 0)], [(3, 0), (5, 5), (5, 0)]) is False, 'different #2'
    assert similar_triangles([[1, 3], [4, 2], [2, 1]], [[2, -2], [0, -3], [-1, -1]]) is True, 'from check'
    assert similar_triangles([[-3, 5], [-5, 3], [-4, 1]], [[-3, -2], [0, 4], [3, -8]]) is True, 'from check 2'
    print("Coding complete? Click 'Check' to earn cool rewards!")
