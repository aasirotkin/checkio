def swap(array, length, pos: int = 0, sequence: str = ''):
    if all(ar1 <= ar2 for ar1, ar2 in zip(array, array[1:])):
        return sequence[:-1]
    if pos >= length:
        pos = 0
    rod1, rod2 = array[pos: pos + 2]
    if rod1 > rod2:
        array[pos: pos + 2] = rod2, rod1
        sequence += '{}{},'.format(pos, pos + 1)
    return swap(array, length, pos + 1, sequence)


def swapsort(array):
    return swap(list(array), len(array) - 1)


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    def check_solution(f, indata):
        result = f(indata)
        array = list(indata[:])
        la = len(array)
        if not isinstance(result, str):
            print("The result should be a string")
            return False
        actions = result.split(",") if result else []
        for act in actions:
            if len(act) != 2 or not act.isdigit():
                print("The wrong action: {}".format(act))
                return False
            i, j = int(act[0]), int(act[1])
            if i >= la or j >= la:
                print("Index error: {}".format(act))
                return False
            if abs(i - j) != 1:
                print("The wrong action: {}".format(act))
                return False
            array[i], array[j] = array[j], array[i]
        if len(actions) > (la * (la - 1)) // 2:
            print("Too many actions. BOOM!")
            return False
        if array != sorted(indata):
            print("The array is not sorted. BOOM!")
            return False
        return True


    assert check_solution(swapsort, (6, 4, 2)), "Reverse simple"
    assert check_solution(swapsort, (1, 2, 3, 4, 5)), "All right!"
    assert check_solution(swapsort, (1, 2, 3, 5, 3)), "One move"
    assert check_solution(swapsort, (1, 2, 3, 4, 5, 6, 7, 8, 9, 9,)), "Edge 3"
    assert check_solution(swapsort, (1, 2, 3, 4, 5, 6, 7, 8, 9, 1,)), "Edge 4"
    assert check_solution(swapsort, (9, 1, 1, 1, 1, 1, 1, 1, 1, 1,)), "Edge 5"
    assert check_solution(swapsort, (5, 8, 5, 3, 7, 8, 1, 5, 1, 4,)), "Extra 3"
    assert check_solution(swapsort, (3, 7, 7, 6, 7, 1, 3, 3, 4, 9,)), "Extra 6"
    assert check_solution(swapsort, (1, 7, 2, 4, 7, 9, 2, 9, 7, 3,)), "Extra 8"
    print('Ok!')
