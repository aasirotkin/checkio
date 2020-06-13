ROMAN = {
    1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V',
    6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X',
    20: 'XX', 30: 'XXX', 40: 'XL', 50: 'L', 60: 'LX',
    70: 'LXX', 80: 'LXXX', 90: 'XC', 100: 'C', 200: 'CC',
    300: 'CCC', 400: 'CD', 500: 'D', 600: 'DC', 700: 'DCC',
    800: 'DCCC', 900: 'CM', 1000: 'M', 2000: 'MM', 3000: 'MMM'
}


def checkio(data):
    ll = [data % p for p in [1, 10, 100, 1000, 10000]]
    ll = [ll[i] - ll[i - 1] for i in range(1, len(ll))]
    return ''.join(ROMAN[l] for l in reversed(ll)
                   if l in ROMAN)


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio(6) == 'VI', '6'
    assert checkio(76) == 'LXXVI', '76'
    assert checkio(499) == 'CDXCIX', '499'
    assert checkio(3888) == 'MMMDCCCLXXXVIII', '3888'
    print('Done! Go Check!')
