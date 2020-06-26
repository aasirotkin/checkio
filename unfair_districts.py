from itertools import combinations_with_replacement as cmb
from itertools import combinations as pure_cmb


def it_is_fine(grid: list, candidates: tuple,
               shift: int, amount_of_people: int) -> bool:
    pure_candidates = {candidate for candidate in candidates
                       if candidate >= 0}
    length = len(pure_candidates)
    if pure_candidates == {1, 5, 9, 13}:
        i = 5
    if length == 0:
        return False
    summation = 0
    for pc in pure_candidates:
        row, col = 0, 0
        while not (row * shift <= pc < (row + 1) * shift):
            row += 1
        col = pc - row * shift if row > 0 else pc
        summation += sum(grid[row][col])
    if summation != amount_of_people:
        return False
    neighbors = 0
    for ci in pure_candidates:
        for cj in pure_candidates:
            b1 = cj - shift == ci
            b2 = ci - shift == cj
            b3 = cj - 1 == ci and cj % shift != 0
            b4 = ci - 1 == cj and ci % shift != 0
            if any([b1, b2, b3, b4]):
                neighbors += 1
    return (neighbors >= length if length == 2 else neighbors > length) \
           or len(pure_candidates) == 1


def make_group(group: tuple) -> tuple:
    return tuple({gr for gr in group if gr >= 0})


def unfair_districts_2(amount_of_people, grid):
    ppp = True
    for gr1, gr2 in zip(grid, grid[1:]):
        if gr1 != gr2:
            ppp = False
            break
    if ppp:
        return []
    people = sum(list(map(lambda x: sum(sum(xi) for xi in x), grid)))
    assert people % amount_of_people == 0
    districts = people // amount_of_people
    districts_names = list('abcdefghijklmnopqrst')
    shift = len(grid[0])
    units_amount = len(grid) * shift
    # all_possibility = pure_cmb(range(units_amount), len(grid))
    all_possibility = cmb([i - 1 for i in range(units_amount + 1)],
                          len(grid) + 1)
    groups = [make_group(group) for group in all_possibility
              if it_is_fine(grid, group, shift, amount_of_people)]
    pure_groups = {i: group for i, group in enumerate(set(groups))}
    combinations = pure_cmb(pure_groups, districts)
    result = [0] * len(grid)
    for i in range(len(result)):
        result[i] = [''] * shift
    res_res = False

    pure_combinations = []
    rng = set(range(units_amount))

    for combo in combinations:
        ss = set()
        for k in combo:
            ss.update(pure_groups[k])
        if ss != rng:
            continue
        winner = []
        dn = -1
        for k in combo:
            win = 0
            dn += 1
            for group in pure_groups[k]:
                row, col = 0, 0
                while not (row * shift <= group < (row + 1) * shift):
                    row += 1
                col = group - row * shift if row > 0 else group
                a = grid[row][col][0]
                b = grid[row][col][1]
                win += a - b
                result[row][col] = '{}'.format(districts_names[dn])
            if win > 0:
                winner.append(1)
            elif win == 0:
                winner.append(0)
            else:
                winner.append(-1)
            # winner.append(1 if win > 0 else -1 if win < 0 else 0)
        if sum(winner) > 0:
            res_res = True
            break

    result = [''.join(ri for ri in r) for r in result]
    print(result, res_res)
    return result if res_res else []


def unfair_districts(number, data):
    height, width = len(data), len(data[1])
    valid = {(x, y) for y in range(width) for x in range(height)}
    out = [[''] * width for _ in range(height)]
    stack = [((0, 0), [((0, 0),)])]
    while stack:
        (x, y), area = stack.pop()
        if len(sum(area, ())) == height * width:
            wins, loses = 0, 0
            for i in area:
                a = sum([data[x][y][0] for x, y in i])
                b = sum([data[x][y][1] for x, y in i])
                wins, loses = wins + (a > b), loses + (a < b)
            if wins <= loses:
                continue
            for k, i in enumerate(area):
                for a, b in i:
                    out[a][b] = str(k)
            return [''.join(j) for j in out]
        last_group = area.pop()
        group_sum = sum(sum([data[i][j] for i, j in last_group], []))
        if group_sum > number:
            continue
        if group_sum == number:
            area, last_group = area + [last_group], ()
        neighbors = {(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)} & valid
        for i in (neighbors - set(sum(area, ()) + last_group)):
            stack += [(i, area + [last_group + (i,)])]
            if len(last_group) in [1, 2]:
                stack += [(last_group[-1], area + [last_group + (i,)])]


if __name__ == '__main__':

    from itertools import chain
    from collections import defaultdict


    def checker(solution, amount_of_people, grid, win_flg=True):

        w, h = len(grid[0]), len(grid)
        size = w * h
        cell_dic = {}

        # make cell_dic
        def adj_cells(cell):
            result = []
            if cell % w != 1 and cell - 1 > 0:
                result.append(cell - 1)
            if cell % w and cell + 1 <= size:
                result.append(cell + 1)
            if (cell - 1) // w:
                result.append(cell - w)
            if (cell - 1) // w < h - 1:
                result.append(cell + w)
            return set(result)

        for i, v in enumerate(chain(*grid)):
            cell_dic[i + 1] = {'vote': v, 'adj': adj_cells(i + 1)}

        answer = solution(amount_of_people, grid)

        if answer == [] and not win_flg:
            return True

        if not isinstance(answer, list):
            print('wrong data type :', answer)
            return False
        else:
            if len(answer) != h:
                print('wrong data length', answer)
                return False
            for an in answer:
                if len(an) != w:
                    print('wrong data length', an)
                    return False

        ds_dic = defaultdict(list)
        for i, r in enumerate(''.join(answer), start=1):
            ds_dic[r].append(i)

        # answer check
        def district_check(d):
            all_cells = set(d[1:])
            next_cells = cell_dic[d[0]]['adj'] & set(d)
            for _ in range(len(d)):
                all_cells -= next_cells
                next_cells = set(chain(*[list(cell_dic[nc]['adj']) for nc in next_cells])) & set(d)
            return not all_cells

        for ch, cells in ds_dic.items():
            dist_people = sum(sum(cell_dic[c]['vote']) for c in cells)
            if not district_check(cells):
                print('wrong district: ', ch)
                return False
            if dist_people != amount_of_people:
                print('wrong people:', ch)
                return False

        # win check
        win, lose = 0, 0
        for part in ds_dic.values():
            vote_a, vote_b = 0, 0
            for p in part:
                a, b = cell_dic[p]['vote']
                vote_a += a
                vote_b += b
            win += vote_a > vote_b
            lose += vote_a < vote_b

        return win > lose


    assert checker(unfair_districts, 5, [
        [[2, 1], [1, 1], [1, 2]],
        [[2, 1], [1, 1], [0, 2]]]), '3x2grid'

    assert checker(unfair_districts, 9, [
        [[0, 3], [3, 3], [1, 1]],
        [[1, 2], [1, 0], [1, 1]],
        [[0, 3], [2, 1], [2, 2]]]), '3x3gid'

    assert checker(unfair_districts, 8, [
        [[1, 1], [2, 0], [2, 0], [3, 3]],
        [[1, 1], [1, 2], [1, 1], [0, 3]],
        [[1, 1], [1, 1], [1, 2], [0, 3]],
        [[1, 1], [1, 1], [1, 1], [2, 0]]]), '4x4gid'

    assert checker(unfair_districts, 3, [
        [[3, 0], [0, 3]],
        [[2, 0], [0, 1]]], False), 'Extra 1'

    assert checker(unfair_districts, 8, [
        [[1, 1], [1, 1], [1, 1], [1, 1]],
        [[1, 1], [1, 1], [1, 1], [1, 1]],
        [[1, 1], [1, 1], [1, 1], [1, 1]],
        [[1, 1], [1, 1], [1, 1], [1, 1]]], False), 'Extra 3'

    assert checker(unfair_districts, 15, [
        [[1, 0], [0, 5], [0, 1], [5, 0], [1, 0]],
        [[0, 2], [0, 3], [0, 2], [0, 4], [2, 0]],
        [[3, 0], [4, 0], [1, 0], [0, 5], [0, 4]],
        [[0, 5], [0, 3], [2, 0], [5, 0], [0, 3]],
        [[0, 4], [0, 1], [0, 2], [0, 3], [0, 4]]]), 'Extra 5'

    print('check done')
