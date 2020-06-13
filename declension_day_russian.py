def declension_day_russian(number: int = 0) -> str:
    """This function with inputted number
       returns the declension of the word
       'day' on The Russian language"""
    if type(number) != int:
        return 'Number = {} is not a number'.format(number)
    if number < 0:
        return 'Number = {} can\'t be less 0'.format(number)
    str_number = str(number)
    str_list = list(str_number)
    last = str_list[-1]
    penultimate = '0'
    if len(str_list) > 1:
        penultimate = str_list[-2]
    if last == '1' or penultimate == '1':
        if penultimate != '1':
            return str_number + ' день'
        else:
            return str_number + ' дней'
    else:
        if last in list('234'):
            return str_number + ' дня'
        else:
            return str_number + ' дней'


for i in range(-1, 367):
    print(declension_day_russian(i))

print(declension_day_russian(list('hello')))
print(declension_day_russian(12345))
print(declension_day_russian(643216232))
print(declension_day_russian())
