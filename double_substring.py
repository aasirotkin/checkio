def double_substring(line):
    length = len(line)
    repeats = [[j - i for j in range(i + 1, length) if line.count(line[i:j]) > 1]
               for i in range(length - 1)]
    return max([max(ri) if ri else 0 for ri in repeats], default=0)


def double_substring_not_my(line):
    for n in range(len(line) // 2, 0, -1):
        for i in range(len(line) - 2 * n + 1):
            if line.count(line[i:i+n], i) > 1:
                return n
    return 0


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert double_substring('aaaa') == 2, "First"
    assert double_substring('abc') == 0, "Second"
    assert double_substring('aghtfghkofgh') == 3, "Third"
    assert double_substring("") == 0, "Extra 1"
    assert double_substring("abababaab") == 3, "Extra 2"
    assert double_substring("arefhjaref!!") == 4, "Extra 3"
    assert double_substring("aa") == 1, "Extra 4"
    assert double_substring("aaaaa") == 2, "Extra 5"
    assert double_substring("hellomymy") == 2, "Extra 6"
    assert double_substring("bobisacoolguyandboblikebobgirlslike") == 4, "Extra 7"
    print('"Run" is good. How is "Check"?')
