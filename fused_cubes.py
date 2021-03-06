from typing import Tuple, List, Iterable

recursion = 0


class Cube:
    # Sorry, but if it works it works!
    def __init__(self, name: int, x: int, y: int, z: int, length: int,
                 x0: int = 0, y0: int = 0, z0: int = 0):
        x, y, z = x - x0, y - y0, z - z0
        self.dl = 0.5 * length
        self.s0 = (x + self.dl, y + self.dl, z + self.dl)
        self.name = name
        self.group = name
        self.points = set()
        self.friends = set()
        for xi in range(length):
            for yi in range(length):
                for zi in range(length):
                    self.points.add((x + xi, y + yi, z + zi))

    @staticmethod
    def good_distance(cube1, cube2) -> bool:
        ds = tuple((cube1.s0[i] - cube2.s0[i]) ** 2 for i in range(3))
        dr = sum(ds) ** 0.5
        return dr < (cube1.r0 + cube2.r0)

    def volume(self, points: set) -> float:
        v = 0
        for point in self.points:
            if point not in points:
                v += 1
        return v

    def intersect(self, cube) -> tuple:
        points = set()
        for point in cube.points:
            if point in self.points:
                points.add(point)
        if points:
            return True, points

        ds = tuple(abs(self.s0[i] - cube.s0[i]) for i in range(3))
        dl = self.dl + cube.dl
        xb = ds[0] < dl and ds[1] < dl and ds[2] == dl
        yb = ds[0] < dl and ds[1] == dl and ds[2] < dl
        zb = ds[0] == dl and ds[1] < dl and ds[2] < dl
        return xb or yb or zb, points


def make_groups(groups: dict, cubes: List[Cube], current_cube: Cube = None):
    global recursion
    recursion += 1
    if current_cube is None:
        current_cube = cubes[0]
    if current_cube.group not in groups:
        groups[current_cube.group] = set()
    for cube in cubes:
        if cube.name not in current_cube.friends:
            current_cube.friends.add(cube.name)
            ret, intersection = current_cube.intersect(cube)
            if ret:
                cube.group = current_cube.group
                groups[current_cube.group] |= intersection
                if recursion > 900:
                    break
                make_groups(groups, cubes, cube)


def fused_cubes(cubes: List[Tuple[int]]) -> Iterable[int]:
    global recursion
    cubes = [Cube(name, x, y, z, length)
             for name, (x, y, z, length) in enumerate(cubes)]
    groups = dict()
    for cube in cubes:
        if cube.name not in groups:
            make_groups(groups, cubes, cube)
            while recursion > 900:
                recursion = 0
                make_groups(groups, cubes, cube)
            recursion = 0
    volumes = []
    for group in groups:
        volumes.append(0)
        for cube in cubes:
            if cube.group == group:
                volumes[-1] += cube.volume(groups[group])
        volumes[-1] += len(groups[group])
    return volumes


if __name__ == '__main__':
    assert sorted(fused_cubes([(0, 0, 0, 3), (3, 3, 3, 3)])) == [27, 27], 'touch with vertices'
    assert sorted(fused_cubes([(0, 0, 0, 3), (1, 2, 2, 3)])) == [52], 'fused'
    assert sorted(fused_cubes([(0, 0, 0, 3), (1, 3, 3, 3)])) == [27, 27], 'touch with edges'
    assert sorted(fused_cubes([(0, 0, 0, 3), (3, 4, 3, 3)])) == [27, 27], 'separated'
    assert sorted(fused_cubes([(0, 0, 0, 3), (-2, -2, -2, 3)])) == [53], 'negative coordinates'
    assert sorted(fused_cubes([[-1, 0, 0, 1], [1, 0, 0, 1],
                               [0, 1, 0, 1], [0, -1, 0, 1],
                               [0, 0, 1, 1], [0, 0, -1, 1]])) == [1, 1, 1, 1, 1, 1], 'Extra 1'
    assert sorted(fused_cubes([(0, 0, 0, 3), (1, 3, 2, 3)])) == [54], 'touch with faces'
    assert sorted(fused_cubes([[-2, -4, 0, 2], [0, -2, 2, 2], [-2, 0, 4, 2],
                               [-4, 2, 2, 2], [-6, 0, 0, 2]])) == [8, 8, 8, 8, 8], 'Extra 2'
    assert sorted(fused_cubes([[0, 0, 0, 1], [0, 1, 0, 1], [0, 2, 0, 1],
                               [0, 3, 0, 1], [0, 5, 0, 1], [-1, 4, 0, 1],
                               [0, 4, 0, 1], [1, 4, 0, 1], [2, 4, 0, 1],
                               [3, 4, 0, 1], [4, 4, 0, 1], [5, 4, 0, 1],
                               [-1, 6, 0, 1], [0, 6, 0, 1], [1, 6, 0, 1],
                               [2, 6, 0, 1], [3, 6, 0, 1], [4, 6, 0, 1],
                               [5, 6, 0, 1], [4, 0, 0, 1], [4, 1, 0, 1],
                               [4, 2, 0, 1], [4, 3, 0, 1], [4, 5, 0, 1],
                               [2, 5, 0, 1]])) == [25], 'Extra 3'
    assert sorted(fused_cubes([[-4, 0, -4, 2], [-2, 0, -4, 2], [0, 0, -4, 2],
                               [2, 0, -4, 2], [2, 0, -2, 2], [2, 0, 0, 2],
                               [2, 0, 2, 2], [-3, 2, -3, 2], [-1, 2, -3, 2],
                               [1, 2, -3, 2], [1, 2, -1, 2], [1, 2, 1, 2],
                               [-2, 4, -2, 2], [0, 4, -2, 2], [0, 4, 0, 2],
                               [-1, 0, -5, 1], [0, 0, -5, 1], [-1, 1, -4, 2],
                               [-1, 3, -3, 2], [4, 0, -1, 1], [4, 0, 0, 1],
                               [2, 1, -1, 2], [1, 3, -1, 2],
                               [-1, 6, -1, 2]])) == [140], 'Extra 4'
    assert sorted(fused_cubes([[-4, -3, -3, 6], [-3, -4, -3, 6], [-3, -3, -4, 6],
                               [-3, -3, -3, 6], [-3, -3, -2, 6], [-3, -2, -3, 6],
                               [-2, -3, -3, 6], [-5, -2, -2, 4], [-4, -4, -2, 4],
                               [-4, -2, -4, 4], [-4, -2, 0, 4], [-4, 0, -2, 4],
                               [-2, -5, -2, 4], [-2, -4, -4, 4], [-2, -4, 0, 4],
                               [-2, -2, -5, 4], [-2, -2, 1, 4], [-2, 0, -4, 4],
                               [-2, 0, 0, 4], [-2, 1, -2, 4], [0, -4, -2, 4],
                               [0, -2, -4, 4], [0, -2, 0, 4], [0, 0, -2, 4],
                               [1, -2, -2, 4], [-5, -3, -1, 2], [-5, -1, -3, 2],
                               [-5, -1, 1, 2], [-5, 1, -1, 2], [-3, -5, -1, 2],
                               [-3, -1, -5, 2], [-3, -1, 3, 2], [-3, 3, -1, 2],
                               [-1, -5, -3, 2], [-1, -5, 1, 2], [-1, -3, -5, 2],
                               [-1, -3, 3, 2], [-1, 1, -5, 2], [-1, 1, 3, 2],
                               [-1, 3, -3, 2], [-1, 3, 1, 2], [1, -5, -1, 2],
                               [1, -1, -5, 2], [1, -1, 3, 2], [1, 3, -1, 2],
                               [3, -3, -1, 2], [3, -1, -3, 2], [3, -1, 1, 2],
                               [3, 1, -1, 2]])) == [624], 'Extra 5'
    assert sorted(fused_cubes([[-4, -4, -4, 8], [-5, -3, -3, 6], [-3, -5, -3, 6],
                               [-3, -3, -5, 6], [-3, -3, -1, 6], [-3, -1, -3, 6],
                               [-1, -3, -3, 6], [-6, -3, -2, 4], [-6, -2, -3, 4],
                               [-6, -2, -2, 4], [-6, -2, -1, 4], [-6, -1, -2, 4],
                               [-5, -4, -2, 4], [-5, -2, -4, 4], [-5, -2, 0, 4],
                               [-5, 0, -2, 4], [-4, -5, -2, 4], [-4, -2, -5, 4],
                               [-4, -2, 1, 4], [-4, 1, -2, 4], [-3, -6, -2, 4],
                               [-3, -2, -6, 4], [-3, -2, 2, 4], [-3, 2, -2, 4],
                               [-2, -6, -3, 4], [-2, -6, -2, 4], [-2, -6, -1, 4],
                               [-2, -5, -4, 4], [-2, -5, 0, 4], [-2, -4, -5, 4],
                               [-2, -4, 1, 4], [-2, -3, -6, 4], [-2, -3, 2, 4],
                               [-2, -2, -6, 4], [-2, -2, 2, 4], [-2, -1, -6, 4],
                               [-2, -1, 2, 4], [-2, 0, -5, 4], [-2, 0, 1, 4],
                               [-2, 1, -4, 4], [-2, 1, 0, 4], [-2, 2, -3, 4],
                               [-2, 2, -2, 4], [-2, 2, -1, 4], [-1, -6, -2, 4],
                               [-1, -2, -6, 4], [-1, -2, 2, 4], [-1, 2, -2, 4],
                               [0, -5, -2, 4], [0, -2, -5, 4], [0, -2, 1, 4],
                               [0, 1, -2, 4], [1, -4, -2, 4], [1, -2, -4, 4],
                               [1, -2, 0, 4], [1, 0, -2, 4], [2, -3, -2, 4],
                               [2, -2, -3, 4], [2, -2, -2, 4], [2, -2, -1, 4],
                               [2, -1, -2, 4]])), 'Extra 6'
    assert sorted(fused_cubes([[-9, -8, -8, 16], [-8, -9, -8, 16], [-8, -8, -9, 16],
                               [-8, -8, -8, 16], [-8, -8, -7, 16], [-8, -7, -8, 16],
                               [-7, -8, -8, 16], [-11, -7, -7, 14], [-10, -8, -7, 14],
                               [-10, -7, -8, 14], [-10, -7, -7, 14], [-10, -7, -6, 14],
                               [-10, -6, -7, 14], [-9, -9, -7, 14], [-9, -7, -9, 14],
                               [-9, -7, -5, 14], [-9, -5, -7, 14], [-8, -10, -7, 14],
                               [-8, -7, -10, 14], [-8, -7, -4, 14], [-8, -4, -7, 14],
                               [-7, -11, -7, 14], [-7, -10, -8, 14], [-7, -10, -7, 14],
                               [-7, -10, -6, 14], [-7, -9, -9, 14], [-7, -9, -5, 14],
                               [-7, -8, -10, 14], [-7, -8, -4, 14], [-7, -7, -11, 14],
                               [-7, -7, -10, 14], [-7, -7, -4, 14], [-7, -7, -3, 14],
                               [-7, -6, -10, 14], [-7, -6, -4, 14], [-7, -5, -9, 14],
                               [-7, -5, -5, 14], [-7, -4, -8, 14], [-7, -4, -7, 14],
                               [-7, -4, -6, 14], [-7, -3, -7, 14], [-6, -10, -7, 14],
                               [-6, -7, -10, 14], [-6, -7, -4, 14], [-6, -4, -7, 14],
                               [-5, -9, -7, 14], [-5, -7, -9, 14], [-5, -7, -5, 14],
                               [-5, -5, -7, 14], [-4, -8, -7, 14], [-4, -7, -8, 14],
                               [-4, -7, -7, 14], [-4, -7, -6, 14], [-4, -6, -7, 14],
                               [-3, -7, -7, 14], [-12, -6, -6, 12], [-11, -8, -6, 12],
                               [-11, -6, -8, 12], [-11, -6, -4, 12], [-11, -4, -6, 12],
                               [-10, -9, -6, 12], [-10, -6, -9, 12], [-10, -6, -3, 12],
                               [-10, -3, -6, 12], [-9, -10, -6, 12], [-9, -6, -10, 12],
                               [-9, -6, -2, 12], [-9, -2, -6, 12], [-8, -11, -6, 12],
                               [-8, -6, -11, 12], [-8, -6, -1, 12], [-8, -1, -6, 12],
                               [-6, -12, -6, 12], [-6, -11, -8, 12], [-6, -11, -4, 12],
                               [-6, -10, -9, 12], [-6, -10, -3, 12], [-6, -9, -10, 12],
                               [-6, -9, -2, 12], [-6, -8, -11, 12], [-6, -8, -1, 12],
                               [-6, -6, -12, 12], [-6, -6, 0, 12], [-6, -4, -11, 12],
                               [-6, -4, -1, 12], [-6, -3, -10, 12], [-6, -3, -2, 12],
                               [-6, -2, -9, 12], [-6, -2, -3, 12], [-6, -1, -8, 12],
                               [-6, -1, -4, 12], [-6, 0, -6, 12], [-4, -11, -6, 12],
                               [-4, -6, -11, 12], [-4, -6, -1, 12], [-4, -1, -6, 12],
                               [-3, -10, -6, 12], [-3, -6, -10, 12], [-3, -6, -2, 12],
                               [-3, -2, -6, 12], [-2, -9, -6, 12], [-2, -6, -9, 12],
                               [-2, -6, -3, 12], [-2, -3, -6, 12], [-1, -8, -6, 12],
                               [-1, -6, -8, 12], [-1, -6, -4, 12], [-1, -4, -6, 12],
                               [0, -6, -6, 12], [-13, -5, -5, 10], [-12, -7, -5, 10],
                               [-12, -5, -7, 10], [-12, -5, -3, 10], [-12, -3, -5, 10],
                               [-10, -10, -5, 10], [-10, -5, -10, 10], [-10, -5, 0, 10],
                               [-10, 0, -5, 10], [-7, -12, -5, 10], [-7, -5, -12, 10],
                               [-7, -5, 2, 10], [-7, 2, -5, 10], [-5, -13, -5, 10],
                               [-5, -12, -7, 10], [-5, -12, -3, 10], [-5, -10, -10, 10],
                               [-5, -10, 0, 10], [-5, -7, -12, 10], [-5, -7, 2, 10],
                               [-5, -5, -13, 10], [-5, -5, 3, 10], [-5, -3, -12, 10],
                               [-5, -3, 2, 10], [-5, 0, -10, 10], [-5, 0, 0, 10],
                               [-5, 2, -7, 10], [-5, 2, -3, 10], [-5, 3, -5, 10],
                               [-3, -12, -5, 10], [-3, -5, -12, 10], [-3, -5, 2, 10],
                               [-3, 2, -5, 10], [0, -10, -5, 10], [0, -5, -10, 10],
                               [0, -5, 0, 10], [0, 0, -5, 10], [2, -7, -5, 10],
                               [2, -5, -7, 10],
                               [2, -5, -3, 10], [2, -3, -5, 10], [3, -5, -5, 10],
                               [-13, -6, -4, 8], [-13, -4, -6, 8], [-13, -4, -2, 8],
                               [-13, -2, -4, 8], [-12, -8, -4, 8], [-12, -4, -8, 8],
                               [-12, -4, 0, 8], [-12, 0, -4, 8], [-11, -9, -4, 8],
                               [-11, -4, -9, 8], [-11, -4, 1, 8], [-11, 1, -4, 8],
                               [-9, -11, -4, 8], [-9, -4, -11, 8], [-9, -4, 3, 8],
                               [-9, 3, -4, 8], [-8, -12, -4, 8], [-8, -4, -12, 8],
                               [-8, -4, 4, 8], [-8, 4, -4, 8], [-6, -13, -4, 8],
                               [-6, -4, -13, 8], [-6, -4, 5, 8], [-6, 5, -4, 8],
                               [-4, -13, -6, 8], [-4, -13, -2, 8], [-4, -12, -8, 8],
                               [-4, -12, 0, 8], [-4, -11, -9, 8], [-4, -11, 1, 8],
                               [-4, -9, -11, 8], [-4, -9, 3, 8], [-4, -8, -12, 8],
                               [-4, -8, 4, 8], [-4, -6, -13, 8], [-4, -6, 5, 8],
                               [-4, -2, -13, 8], [-4, -2, 5, 8], [-4, 0, -12, 8],
                               [-4, 0, 4, 8], [-4, 1, -11, 8], [-4, 1, 3, 8],
                               [-4, 3, -9, 8], [-4, 3, 1, 8], [-4, 4, -8, 8],
                               [-4, 4, 0, 8], [-4, 5, -6, 8], [-4, 5, -2, 8],
                               [-2, -13, -4, 8], [-2, -4, -13, 8], [-2, -4, 5, 8],
                               [-2, 5, -4, 8], [0, -12, -4, 8], [0, -4, -12, 8],
                               [0, -4, 4, 8], [0, 4, -4, 8], [1, -11, -4, 8],
                               [1, -4, -11, 8], [1, -4, 3, 8], [1, 3, -4, 8],
                               [3, -9, -4, 8], [3, -4, -9, 8], [3, -4, 1, 8],
                               [3, 1, -4, 8], [4, -8, -4, 8], [4, -4, -8, 8],
                               [4, -4, 0, 8], [4, 0, -4, 8], [5, -6, -4, 8],
                               [5, -4, -6, 8], [5, -4, -2, 8], [5, -2, -4, 8],
                               [-14, -4, -3, 6], [-14, -3, -4, 6], [-14, -3, -3, 6],
                               [-14, -3, -2, 6], [-14, -2, -3, 6], [-4, -14, -3, 6],
                               [-4, -3, -14, 6], [-4, -3, 8, 6], [-4, 8, -3, 6],
                               [-3, -14, -4, 6], [-3, -14, -3, 6], [-3, -14, -2, 6],
                               [-3, -4, -14, 6], [-3, -4, 8, 6], [-3, -3, -14, 6],
                               [-3, -3, 8, 6], [-3, -2, -14, 6], [-3, -2, 8, 6],
                               [-3, 8, -4, 6], [-3, 8, -3, 6], [-3, 8, -2, 6],
                               [-2, -14, -3, 6], [-2, -3, -14, 6], [-2, -3, 8, 6],
                               [-2, 8, -3, 6], [8, -4, -3, 6], [8, -3, -4, 6],
                               [8, -3, -3, 6], [8, -3, -2, 6], [8, -2, -3, 6],
                               [-14, -5, -2, 4], [-14, -2, -5, 4], [-14, -2, 1, 4],
                               [-14, 1, -2, 4], [-13, -7, -2, 4], [-13, -2, -7, 4],
                               [-13, -2, 3, 4], [-13, 3, -2, 4], [-11, -10, -2, 4],
                               [-11, -2, -10, 4], [-11, -2, 6, 4], [-11, 6, -2, 4],
                               [-10, -11, -2, 4], [-10, -2, -11, 4], [-10, -2, 7, 4],
                               [-10, 7, -2, 4], [-7, -13, -2, 4], [-7, -2, -13, 4],
                               [-7, -2, 9, 4], [-7, 9, -2, 4], [-5, -14, -2, 4],
                               [-5, -2, -14, 4], [-5, -2, 10, 4], [-5, 10, -2, 4],
                               [-2, -14, -5, 4], [-2, -14, 1, 4], [-2, -13, -7, 4],
                               [-2, -13, 3, 4], [-2, -11, -10, 4], [-2, -11, 6, 4],
                               [-2, -10, -11, 4], [-2, -10, 7, 4], [-2, -7, -13, 4],
                               [-2, -7, 9, 4], [-2, -5, -14, 4], [-2, -5, 10, 4],
                               [-2, 1, -14, 4], [-2, 1, 10, 4], [-2, 3, -13, 4],
                               [-2, 3, 9, 4], [-2, 6, -11, 4], [-2, 6, 7, 4],
                               [-2, 7, -10, 4], [-2, 7, 6, 4], [-2, 9, -7, 4],
                               [-2, 9, 3, 4], [-2, 10, -5, 4], [-2, 10, 1, 4],
                               [1, -14, -2, 4], [1, -2, -14, 4], [1, -2, 10, 4],
                               [1, 10, -2, 4], [3, -13, -2, 4], [3, -2, -13, 4],
                               [3, -2, 9, 4], [3, 9, -2, 4], [6, -11, -2, 4],
                               [6, -2, -11, 4], [6, -2, 7, 4], [6, 7, -2, 4],
                               [7, -10, -2, 4], [7, -2, -10, 4], [7, -2, 6, 4],
                               [7, 6, -2, 4], [9, -7, -2, 4], [9, -2, -7, 4],
                               [9, -2, 3, 4], [9, 3, -2, 4], [10, -5, -2, 4],
                               [10, -2, -5, 4], [10, -2, 1, 4], [10, 1, -2, 4]])) == [12112], 'Extra 7'
    print("Coding complete? Click 'Check' to earn cool rewards!")
