from typing import List


class Node:
    def __init__(self, name: int, row: int, col: int):
        self.name = name
        self.row = row
        self.col = col
        self.friends = dict()


class OpenLabyrinth:
    def __init__(self, labyrinth: List[List[int]]):
        self.labyrinth = labyrinth
        rows, cols = range(len(labyrinth)), range(len(labyrinth[0]))
        self.valid_route = {(i, j) for i in rows for j in cols
                            if self.labyrinth[i][j] == 0}
        assert all([r != 0 and c != 0 and
                    r != max(rows) and c != max(cols)
                    for r, c in self.valid_route])
        self.path = {(1, 0): 'S', (-1, 0): 'N', (0, -1): 'W', (0, 1): 'E'}
        self.reverse_path = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        self.nodes = dict()
        self.nodes[0] = Node(0, 1, 1)
        self.nodes[1] = Node(1, 10, 10)
        self.make_nodes()
        self.make_connections()

    def reverse_name(self, name: str) -> str:
        return ''.join(self.reverse_path[n]
                       if n in self.reverse_path else 'Error'
                       for n in reversed(name))

    def path_name(self, row_old: int, col_old: int,
                  row_new: int, col_new: int) -> str:
        path_key = (row_new - row_old, col_new - col_old)
        return self.path[path_key] if path_key in self.path else 'Error'

    def neighbours(self, row: int, col: int,
                   row_old: int = -1, col_old: int = -1) -> list:
        return [(r, c)
                for r, c in [(row, col - 1), (row - 1, col),
                             (row, col + 1), (row + 1, col)]
                if self.labyrinth[r][c] == 0 and
                (r != row_old or c != col_old)]

    def is_it_new_node(self, row: int, col: int):
        return all([node.row != row or node.col != col
                    for name, node in self.nodes.items()])

    def find_friends(self, row_old: int, col_old: int,
                     row_new: int, col_new: int, path: list = None) -> tuple:
        neighbours = self.neighbours(row_new, col_new, row_old, col_old)
        length = len(neighbours)
        if length == 1:
            row_old, col_old = row_new, col_new
            row_new, col_new = neighbours.pop()
            path.append(self.path_name(row_old, col_old, row_new, col_new))
            return self.find_friends(row_old, col_old, row_new, col_new, path)
        else:
            return row_new, col_new

    def make_nodes(self):
        for r, c in self.valid_route:
            neighbours = self.neighbours(r, c)
            if len(neighbours) >= 3 and self.is_it_new_node(r, c):
                name = len(self.nodes)
                self.nodes[name] = Node(name, r, c)

    def node_name(self, row: int, col: int) -> int:
        for name, node in self.nodes.items():
            if node.row == row and node.col == col:
                return name
        return -1

    def make_connections(self):
        for name, node in self.nodes.items():
            neighbours = self.neighbours(node.row, node.col)
            while neighbours:
                nr, nc = neighbours.pop()
                path = [self.path_name(node.row, node.col, nr, nc)]
                pr, pc = self.find_friends(node.row, node.col, nr, nc, path)
                node_name = self.node_name(pr, pc)
                if node_name >= 0:
                    node.friends[node_name] = ''.join(p for p in path)

    def __find_route(self, node_from_name: int, node_to_name: int,
                     route: list = None) -> tuple:
        if route is None:
            route = []
        for name_i, route_i in self.nodes[node_from_name].friends.items():
            if name_i in route:
                continue
            route.append(name_i)
            if name_i == node_to_name:
                break
            route, node_to_name = self.__find_route(name_i, node_to_name, route)
            if node_to_name in route:
                break
            else:
                del route[-1]
        return route, node_to_name

    def find_route(self, node_from_name: int, node_to_name: int) -> str:
        routes = [self.__find_route(node_from_name, friend, [node_from_name])
                  for friend in self.nodes[node_to_name].friends]
        route, name = min([r for r in routes if len(r[0]) > 0],
                          key=lambda x: len(x[0]), default=([], node_from_name))
        string_route = ''.join([self.nodes[n1].friends[n2]
                                for n1, n2 in zip(route, route[1:])])
        if node_to_name not in route:
            last_move = reversed(self.nodes[node_to_name].friends[name])
            string_route += ''.join([self.reverse_path[lm]
                                     for lm in last_move])
        return string_route


def checkio(maze_map: List[List[int]]) -> str:
    open_labyrinth = OpenLabyrinth(maze_map)
    route = open_labyrinth.find_route(0, 1)
    return route


if __name__ == '__main__':
    # This code using only for self-checking and not necessary for auto-testing
    def check_route(func, labyrinth):
        MOVE = {"S": (1, 0), "N": (-1, 0), "W": (0, -1), "E": (0, 1)}
        # copy maze
        route = func([row[:] for row in labyrinth])
        pos = (1, 1)
        goal = (10, 10)
        for i, d in enumerate(route):
            move = MOVE.get(d, None)
            if not move:
                print("Wrong symbol in route")
                return False
            pos = pos[0] + move[0], pos[1] + move[1]
            if pos == goal:
                if i == (len(route) - 1):
                    return True
                else:
                    print("Player was close as he had never been before")
                    return False
            if pos == goal and i == (len(route) - 1):
                return True
            if labyrinth[pos[0]][pos[1]] == 1:
                print("Player in the pit")
                return False
        print("Player did not reach exit")
        return False

    # These assert are using only for self-testing as examples.
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1],
        [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "First maze"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Empty maze"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Dotted maze"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Need left maze"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "The big dead end."
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Extra 1"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Extra 2"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1],
        [1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
        [1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1],
        [1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1],
        [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Extra 3"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Extra 4"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Up and down maze"

    print("The local tests are done.")
