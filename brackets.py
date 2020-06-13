from re import search, sub


pairs = {'(': ')',
         '[': ']',
         '{': '}'}


def good_brackets(expression):
    r = ('(?:\([^\[\]{}()]*\){1})|'
         '(?:\[[^\[\]{}()]*\]{1})|'
         '(?:\{[^\[\]{}()]*\}{1})')
    while search(r, expression):
        expression = sub(r, '', expression)
    return not search(r'[\[\]{}()]', expression)


def intersection(i, j, stack):
    for k in range(0, len(stack) - 1, 2):
        if (i - 1) == stack[k] and \
                (i + 1) == stack[k + 1] or \
                (j - 1) == stack[k] and \
                (j + 1) == stack[k + 1]:
            return True
    return False


def backward(i, length, a, stack):
    for j in range(i + 1, length):
        if j not in stack and \
                pairs[a[i]] == a[j]:
            if not intersection(i, j, stack):
                stack.append(i)
                stack.append(j)
                return True
    return False


def remove_brackets(a):
    stack = list()
    length = len(a)

    for i in reversed(range(length)):
        if a[i] in pairs:
            backward(i, length, a, stack)

    return ''.join(a[i] for i in range(len(a))
                   if i in stack)


print(remove_brackets('(()()'))
print(remove_brackets('{{{}}}'))
print(remove_brackets('[][[[[[[[[[[[[[[[[[[[[[[[['))
print(remove_brackets('[[(}]]'))
print(remove_brackets('[[{}()]]'))
print(remove_brackets('[[[[[['))
print(remove_brackets("[(()]"))
print(remove_brackets("[(])"))
