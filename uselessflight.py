from typing import List, Dict, Tuple


def find_lower_cost(graph: Dict, data: Tuple):
    dist = {a: data[2] for a in graph}
    visited = {a: False for a in graph}
    dist[data[0]] = 0

    while True:
        u = ''
        sd = data[2]
        for c, v in visited.items():
            if not v and dist[c] < sd:
                sd = dist[c]
                u = c
        if not u: break
        visited[u] = True

        for g in graph:
            v = u
            w = data[2]
            for r in graph[u]:
                if g in r:
                    v, w = r
                    break
            if v == u: continue

            newLen = dist[u] + w
            if newLen < dist[v]:
                dist[v] = newLen

    del visited
    return dist[data[1]]


def useless_flight(schedule: List) -> List:
    graph = {}
    for sc in schedule:
        if sc[0] not in graph: graph[sc[0]] = []
        if sc[1] not in graph: graph[sc[1]] = []

        graph[sc[0]].append((sc[1], sc[2]))
        graph[sc[1]].append((sc[0], sc[2]))

    return [i for i, sc in enumerate(schedule)
            if find_lower_cost(graph, sc) < sc[2]]


if __name__ == '__main__':
    print("Example:")
    print(useless_flight([['A', 'B', 50],
                          ['B', 'C', 40],
                          ['A', 'C', 100]]))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert useless_flight([['A', 'B', 50],
                           ['B', 'C', 40],
                           ['A', 'C', 100]]) == [2]
    assert useless_flight([['A', 'B', 50],
                           ['B', 'C', 40],
                           ['A', 'C', 90]]) == []
    assert useless_flight([['A', 'B', 50],
                           ['B', 'C', 40],
                           ['A', 'C', 40]]) == []
    assert useless_flight([['A', 'C', 10],
                           ['C', 'B', 10],
                           ['C', 'E', 10],
                           ['C', 'D', 10],
                           ['B', 'E', 25],
                           ['A', 'D', 20],
                           ['D', 'F', 50],
                           ['E', 'F', 90]]) == [4, 7]
    print("Coding complete? Click 'Check' to earn cool rewards!")
