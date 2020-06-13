def is_family(names):
    family = dict()
    sons = []
    errors = []

    for father, son in names:
        if father not in family:
            family[father] = []
        if son not in sons:
            sons.append(son)
        else:
            errors.append(f'{son} can\'t have two fathers')
        family[father].append(son)

    sons.clear()

    for father, children in family.items():
        for child in children:
            if child in family and child not in sons:
                sons.append(child)
            if child in family:
                if father in family[child]:
                    errors.append(f'{child} can\'t be a father for {father}')
                for nephew in family[child]:
                    if nephew in children:
                        errors.append(f'{child} can\'t be a father for his brother {nephew}')

    if len(family) != (len(sons) + 1):
        errors.append('Extra family')

    return not errors


if __name__ == "__main__":
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert is_family([
        ['Logan', 'Mike']
    ]) is True, 'One father, one son'
    assert is_family([
        ['Logan', 'Mike'],
        ['Logan', 'Jack']
    ]) is True, 'Two sons'
    assert is_family([
        ['Logan', 'Mike'],
        ['Logan', 'Jack'],
        ['Mike', 'Alexander']
    ]) is True, 'Grandfather'
    assert is_family([
        ['Logan', 'Mike'],
        ['Logan', 'Jack'],
        ['Mike', 'Logan']
    ]) is False, 'Can you be a father to your father?'
    assert is_family([
        ['Logan', 'Mike'],
        ['Logan', 'Jack'],
        ['Mike', 'Jack']
    ]) is False, 'Can you be a father to your brother?'
    assert is_family([
        ['Logan', 'William'],
        ['Logan', 'Jack'],
        ['Mike', 'Alexander']
    ]) is False, 'Looks like Mike is stranger in Logan\'s family'
    print("Looks like you know everything. It is time for 'Check'!")
