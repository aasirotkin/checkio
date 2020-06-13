from datetime import datetime as dt

df = '%d.%m.%Y'
now = dt.strptime('01.01.2018', df)


class Person:
    def __init__(self, first_name, last_name, birth_date, job, working_years, salary, country, city, gender='unknown'):
        self.about = first_name, last_name, birth_date, job, working_years, salary, country, city, gender

    def name(self) -> str:
        return f'{self.about[0]} {self.about[1]}'

    def age(self) -> int:
        return int((now - dt.strptime(self.about[2], df))
                   .days / 365)

    def work(self) -> str:
        appendix = 'Is a '
        if self.about[8] == 'male':
            appendix = 'He is a '
        elif self.about[8] == 'female':
            appendix = 'She is a '
        return f'{appendix}{self.about[3]}'

    def money(self) -> str:
        m = str(self.about[4] * self.about[5] * 12)
        l = len(m) - 1
        return ''.join(m[l - i] if i % 3 != 0 or i == 0
                       else f'{m[l - i]} '
                       for i in range(l, -1, -1))

    def home(self) -> str:
        return f'Lives in {self.about[7]}, {self.about[6]}'


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    p1 = Person("John", "Smith", "19.09.1979", "welder", 15, 3600, "Canada", "Vancouver", "male")
    p2 = Person("Hanna Rose", "May", "05.12.1995", "designer", 2.2, 2150, "Austria", "Vienna")
    assert p1.name() == "John Smith", "Name"
    assert p1.age() == 38, "Age"
    assert p2.work() == "Is a designer", "Job"
    assert p1.money() == "648 000", "Money"
    assert p2.home() == "Lives in Vienna, Austria", "Home"
    print("Coding complete? Let's try tests!")
