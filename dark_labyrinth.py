class DarkLabyrinth:
    player = "P"
    wall = "X"
    unknown = "?"
    forbidden = 'F'
    end = "E"
    road = "."
    analog = {player: 1, road: 0, wall: -1, end: -2, unknown: -3}
    directions = {'N', 'E', 'S', 'W'}

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.map = []
            cls.path_history = []
            cls.is_inited = False
            cls.instance = super(DarkLabyrinth, cls).__new__(cls)
        return cls.instance

    def update_map(self, visible_map, dpr, dpc):
        if dpr < 0:
            for h in range(-dpr):
                new_part = [self.analog[self.unknown]]*len(self.map[0])
                self.map.insert(0, new_part)

        dh = dpr + len(visible_map) - len(self.map)
        if dh > 0:
            for h in range(dh):
                new_part = [self.analog[self.unknown]] * len(self.map[0])
                self.map.append(new_part)

        height = max(len(visible_map), len(self.map))

        for h in range(len(self.map), height):
            new_part = [self.analog[self.unknown]]*len(self.map[0])
            self.map.append(new_part)

        if dpc < 0:
            for m in self.map:
                new_part = [self.analog[self.unknown]]*(-dpc)
                right_part = m.copy()
                m.clear()
                m += new_part
                m += right_part

        dw = dpc + len(visible_map[0]) - len(self.map[0])
        if dw > 0:
            for m in self.map:
                new_part = [self.analog[self.unknown]]*dw
                m += new_part

        width = max(len(visible_map[0]), len(self.map[0]))

        if width > len(self.map[0]):
            dw = width - len(self.map[0])
            for m in self.map:
                new_part = [self.analog[self.unknown]]*dw
                m += new_part

        for r in range(len(visible_map)):
            for c in range(len(visible_map[0])):
                if dpr > 0:
                    dr = r + dpr
                else:
                    dr = r
                if dpc > 0:
                    dc = c + dpc
                else:
                    dc = c
                symbol = max(self.map[dr][dc], visible_map[r][c])
                self.map[dr][dc] = symbol

    def make_map(self, visible_map) -> list:
        return [[self.analog[visible_map[row][col]]
                 for col in range(len(visible_map[0]))]
                for row in range(len(visible_map))]

    def find_player(self, visible_map) -> tuple:
        for row in range(len(visible_map)):
            for col in range(len(visible_map[0])):
                if visible_map[row][col] == self.player:
                    return row, col
        return -1, -1

    def __init__(self, visible_map):
        if not self.is_inited:
            self.is_inited = True
            self.map = self.make_map(visible_map)
            self.pr, self.pc = self.find_player(visible_map)
        else:
            new_map = self.make_map(visible_map)
            pr, pc = self.find_player(visible_map)
            hpr, hpc = self.path_history[-1][-1]
            dpr, dpc = hpr - pr, hpc - pc
            self.update_map(new_map, dpr, dpc)
            if dpr >= 0:
                self.pr = hpr
            else:
                self.pr = hpr - dpr
            if dpc >= 0:
                self.pc = hpc
            else:
                self.pc = hpc - dpc
        self.grid = {(row, col) for row in range(len(self.map))
                     for col in range(len(self.map[0]))}

    def neighbours(self, row: int, col: int) -> set:
        return {(row - 1, col), (row, col + 1),
                (row + 1, col), (row, col - 1)} & self.grid

    @staticmethod
    def direction_name(row_old: int, col_old: int,
                       row_new: int, col_new: int) -> str:
        if row_old > row_new:
            return 'N'
        elif row_old < row_new:
            return 'S'
        elif col_old > col_new:
            return 'W'
        elif col_old < col_new:
            return 'E'
        else:
            return 'Error'

    def go_on(self, row, col) -> bool:
        return (self.map[row][col] >= 0 or
                self.map[row][col] == self.analog[self.unknown] or
                self.map[row][col] == self.analog[self.end])

    def find(self, current_row: int, current_col: int,
             path: list = None, depth: int = 0) -> list:
        if path is None:
            path = []

        if self.map[current_row][current_col] == self.analog[self.unknown] or \
                self.map[current_row][current_col] == self.analog[self.end] or \
                depth > 50:
            path.append((current_row, current_col))
            return path

        neighbours = []
        for row, col in self.neighbours(current_row, current_col):
            if (row, col) in path:
                continue
            if not self.go_on(row, col):
                continue
            neighbours.append((row, col))

        if len(neighbours) > 0:
            new_path = [self.find(row, col, [(current_row, current_col)], depth+1)
                        for row, col in neighbours]
            while [] in new_path:
                new_path.remove([])
            if len(new_path) == 0:
                path.clear()
            else:
                # for np in new_path:
                #     for r, c in np:
                #         if self.map[r][c] == self.analog[self.end]:
                #             path += np
                #             return path
                path += min([path_i for path_i in new_path if len(path_i) > 0],
                            key=lambda l: sum([self.map[lr][lc] for lr, lc in l]))
        else:
            path.append((current_row, current_col))

        return path

    def next_move(self) -> str:
        path = self.find(self.pr, self.pc)

        pr, pc = path[-1]
        if self.map[pr][pc] == self.analog[self.unknown]:
            del path[-1]

        self.path_history.append(path)
        string_path = ''.join(self.direction_name(row_1, col_1, row_2, col_2)
                              for (row_1, col_1), (row_2, col_2) in zip(path, path[1:]))

        for i, (pr, pc) in enumerate(path):
            if self.map[pr][pc] >= 0:
                self.map[pr][pc] += 1
            elif self.map[pr][pc] == self.analog[self.end]:
                self.is_inited = False
                self.path_history.clear()
                break

        return string_path


def find_path(visible):
    return DarkLabyrinth(visible).next_move()


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    DIR = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}
    PLAYER = "P"
    WALL = "X"
    UNKNOWN = "?"
    EXIT = "E"
    EMPTY = "."
    MAX_STEP = 250

    def clear_zone(zone):
        return [row for row in zone if not all(el == UNKNOWN for el in row)]

    def get_visible(maze, player):
        grid = [["?" for _ in range(len(row))] for row in maze]
        grid[player[0]][player[1]] = PLAYER
        for direction, diff in DIR.items():
            r, c = player
            while maze[r][c] != WALL:
                r, c = r + diff[0], c + diff[1]
                grid[r][c] = maze[r][c]
                if direction in "NS":
                    grid[r + DIR["W"][0]][c + DIR["W"][1]] = maze[r + DIR["W"][0]][c + DIR["W"][1]]
                    grid[r + DIR["E"][0]][c + DIR["E"][1]] = maze[r + DIR["E"][0]][c + DIR["E"][1]]
                else:
                    grid[r + DIR["S"][0]][c + DIR["S"][1]] = maze[r + DIR["S"][0]][c + DIR["S"][1]]
                    grid[r + DIR["N"][0]][c + DIR["N"][1]] = maze[r + DIR["N"][0]][c + DIR["N"][1]]
        grid = clear_zone(list(zip(*clear_zone(grid))))
        return tuple("".join(trow) for trow in zip(*grid))

    def initial(maze, player):
        return maze, get_visible(maze, player)

    def checker(func, player, maze):
        step = 0
        while True:
            result = func(get_visible(maze, player))
            if not isinstance(result, str) or any(ch not in DIR.keys() for ch in result):
                print("The function should return a string with directions.")
                return False

            for act in result:
                if step >= MAX_STEP:
                    print("You are tired and your flashlight is off. Bye bye.")
                    return False
                r, c = player[0] + DIR[act][0], player[1] + DIR[act][1]
                if maze[r][c] == WALL:
                    print("BAM! You in the wall at {}, {}.".format(r, c))
                    return False
                elif maze[r][c] == EXIT:
                    print("GRATZ!")
                    return True
                else:
                    player = r, c
                    step += 1

    assert checker(find_path, (2, 2), [
        "XXXXXXXXXXXXXXX",
        "XXX...........X",
        "X...XXXXXXXXX.X",
        "X.X.X.......X.X",
        "X.X.X.X.X.X.X.X",
        "X.X.X.X.X.X.X.X",
        "X.....XXXXX...X",
        "X.X.X.......X.X",
        "X.X.XXXX.X.XX.X",
        "X.X.X..X.X.X..X",
        "X...XX.X.XXXX.X",
        "X.X..X.X....X.X",
        "X.XXXX.XXXXXX.X",
        "X........XE...X",
        "XXXXXXXXXXXXXXX"
    ]), "Big"
    assert checker(find_path, (10, 10), [
        "XXXXXXXXXXXX",
        "XX...X.....X",
        "X..X.X.X.X.X",
        "X.XX.X.X.X.X",
        "X..X.X.X.X.X",
        "XX.X.X.X.X.X",
        "X..X.X.X.X.X",
        "X.XX.X.X.X.X",
        "X..X.X.X.X.X",
        "XX.X.X.X.X.X",
        "XE.X.....X.X",
        "XXXXXXXXXXXX",
    ]), "Up down"
    assert checker(find_path, (1, 4), [
        "XXXXXXXXXX",
        "X....X...X",
        "X.XXXX.X.X",
        "X....X.X.X",
        "X.XXXX.X.X",
        "X.X....X.X",
        "X.XXEX.X.X",
        "X.XXXXXX.X",
        "X........X",
        "XXXXXXXXXX",
    ]), "First"
    assert checker(find_path, (1, 1), [
        "XXXXXXX",
        "X.....X",
        "X.X.X.X",
        "X.....X",
        "X.X.X.X",
        "X.X.E.X",
        "XXXXXXX",
    ]), "Simple"
    assert checker(find_path, (8, 5), [
        "XXXXXXXXXXXXXXX",
        "X...X.....XXXXX",
        "XXX.X.XXX..XXXX",
        "X...X..XXX..XXX",
        "X.XXXX.X.XX..XX",
        "X.X.......XXE.X",
        "X.XXXX.XXXXXX.X",
        "X....XXX....X.X",
        "XXXX...X.XX...X",
        "X..XXX.X.XX.X.X",
        "XX..XX.X..XXX.X",
        "XXX..X.XX.XX..X",
        "X.XX...X..X..XX",
        "X....X...XX.XXX",
        "XXXXXXXXXXXXXXX"
    ]), "Random"

