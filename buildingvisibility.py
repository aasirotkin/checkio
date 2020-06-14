# https://py.checkio.org/en/mission/buildings-visibility/

class Rect:
    def __init__(self, x1: float, x2: float,
                 y2: float, z: float):
        self.x1 = x1
        self.y1 = 0.0
        self.x2 = x2
        self.y2 = y2
        self.z = z


class Building(Rect):
    def __init__(self, building: list):
        super(Building, self).__init__(building[0], building[2],
                                       building[4], building[1])

    def is_still_visible(self, building: Rect) -> bool:
        if self.z > building.z:
            if building.x1 <= self.x1 <= building.x2:
                self.x1 = building.x2
                return self.x1 < self.x2
            elif building.x1 <= self.x2 <= building.x2:
                self.x2 = building.x1
                return self.x1 < self.x2
        return True

    def is_visible(self, buildings: list):
        return all(self.is_still_visible(building) or building.y2 < self.y2
                   for building in buildings if building != self)


def checkio(buildings):
    buildings = [Building(building) for building in buildings]
    buildings.sort(key=lambda x: x.y2)
    return len([1 for build in buildings if build.is_visible(buildings)])


if __name__ == '__main__':
    assert checkio([
        [1, 1, 4, 5, 3.5],
        [2, 6, 4, 8, 5],
        [5, 1, 9, 3, 6],
        [5, 5, 6, 6, 8],
        [7, 4, 10, 6, 4],
        [5, 7, 10, 8, 3]
    ]) == 5, "First"
    assert checkio([
        [1, 1, 11, 2, 2],
        [2, 3, 10, 4, 1],
        [3, 5, 9, 6, 3],
        [4, 7, 8, 8, 2]
    ]) == 2, "Second"
    assert checkio([
        [1, 1, 3, 3, 6],
        [5, 1, 7, 3, 6],
        [9, 1, 11, 3, 6],
        [1, 4, 3, 6, 6],
        [5, 4, 7, 6, 6],
        [9, 4, 11, 6, 6],
        [1, 7, 11, 8, 3.25]
    ]) == 4, "Third"
    assert checkio([
        [0, 0, 1, 1, 10]
    ]) == 1, "Alone"
    assert checkio([
        [2, 2, 3, 3, 4],
        [2, 5, 3, 6, 4]
    ]) == 1, "Shadow"
    assert checkio([
        [1, 1, 3, 3, 20],
        [3, 4, 5, 6, 10],
        [5, 1, 7, 3, 20],
        [1, 7, 7, 9, 20]
    ]) == 4, "Extra 1"
