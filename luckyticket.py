from itertools import product
from re import sub


def make_groups(length: int) -> list:
    return sorted({''.join(str(j) for j in i if j != 0)
                   for i in product(range(length+1), repeat=length)
                   if sum(i) == length}, reverse=True)


def list_number(sequence: str, group: str) -> list:
    i, num = 0, []
    for shift in group:
        i_shift = int(shift)
        num.append(str(int(sequence[i:i + i_shift])))
        i += i_shift
    return num


def make_numbers(sequence: str, group: list) -> list:
    return [list_number(sequence, g) for g in group]


def make_operations(length: int) -> list:
    return list(product(['+', '-', '*', '/'], repeat=length))


def calculate(numbers: list, operations: list, stop: int) -> bool:
    for operations_i in operations:
        procedure_1 = ''.join(numbers[i]+operations_i[i]
                              for i in range(len(operations_i))) + numbers[-1]
        procedure_2 = sub(r'(\d+[+-]\d+)', r'(\1)', procedure_1)
        procedure_3 = sub(r'\*(.*)', r'*(\1)', procedure_2)

        try:
            if ('/0' not in procedure_1 and round(eval(procedure_1), 1) == stop) or \
                    ('/0' not in procedure_2 and round(eval(procedure_2), 1) == stop) or \
                    ('/0' not in procedure_3 and round(eval(procedure_3), 1) == stop):
                return True
        except ZeroDivisionError:
            pass
    return False


def checkio(data):
    numbers = make_numbers(data, make_groups(len(data)))
    for number in numbers:
        operations = make_operations(len(number)-1)
        if calculate(number, operations, 100):
            return False
    return True


# These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio('205') is False, "Home test 1"
    assert checkio('100') is False, "Home test 2"
    assert checkio('254') is False, "Home test 3"
    assert checkio('595347') is False, "(5 + ((9 / (3 / 34)) - 7)) = 100"
    assert checkio('271353') is False, "(2 - (7 * (((1 / 3) - 5) * 3))) = 100"
    assert checkio("000955") is False, "CheckIo test"
    assert checkio("100479") is False, "CheckIo test 2"
    assert checkio('000000') is True, "All zeros"
    assert checkio('707409') is True, "You can not transform it to 100"
    assert checkio("100478") is True, "CheckIo test 3"
    assert checkio("836403") is False, "CheckIo test 4"
    assert checkio("240668") is False, "CheckIo test 5"
    assert checkio("392039") is False, "CheckIo test 6"
