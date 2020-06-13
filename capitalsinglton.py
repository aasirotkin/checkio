class Capital:
    def __new__(cls, capital_name):
        if not hasattr(cls, 'instance'):
            cls.capital_name = capital_name
            cls.instance = super(Capital, cls).__new__(cls)
        return cls.instance

    def name(self) -> str:
        return self.capital_name


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    ukraine_capital_1 = Capital("Kyiv")
    ukraine_capital_2 = Capital("London")
    ukraine_capital_3 = Capital("Marocco")

    assert ukraine_capital_2 is ukraine_capital_1
    assert ukraine_capital_3 is ukraine_capital_1

    assert ukraine_capital_2.name() == "Kyiv"
    assert ukraine_capital_3.name() == "Kyiv"

    print("Coding complete? Let's try tests!")
