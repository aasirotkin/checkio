def factory(obj, *args, **kwargs):
    return obj(*args, **kwargs)


class AbstractCook:
    def __init__(self, food: str, drink: str):
        self.food = food
        self.drink = drink
        self.food_price = 0
        self.drink_price = 0

    def __call__(self, *args, **kwargs):
        return AbstractCook(food=self.food, drink=self.drink)

    def total(self):
        return '{Food}: {f_price}, {Drink}: {d_price}, Total: {t_price}'.format(
            Food=self.food,
            f_price=self.food_price,
            Drink=self.drink,
            d_price=self.drink_price,
            t_price=(self.food_price+self.drink_price)
        )

    def add_food(self, amount, price):
        self.food_price += amount * price

    def add_drink(self, amount, price):
        self.drink_price += amount * price


JapaneseCook = factory(AbstractCook, food='Sushi', drink='Tea')
RussianCook = factory(AbstractCook, food='Dumplings', drink='Compote')
ItalianCook = factory(AbstractCook, food='Pizza', drink='Juice')


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    client_1 = JapaneseCook()
    client_1.add_food(2, 30)
    client_1.add_food(3, 15)
    client_1.add_drink(2, 10)

    client_2 = RussianCook()
    client_2.add_food(1, 40)
    client_2.add_food(2, 25)
    client_2.add_drink(5, 20)

    client_3 = ItalianCook()
    client_3.add_food(2, 20)
    client_3.add_food(2, 30)
    client_3.add_drink(2, 10)

    assert client_1.total() == "Sushi: 105, Tea: 20, Total: 125"
    assert client_2.total() == "Dumplings: 90, Compote: 100, Total: 190"
    assert client_3.total() == "Pizza: 100, Juice: 20, Total: 120"
    print("Coding complete? Let's try tests!")
