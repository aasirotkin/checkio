from abc import ABCMeta, abstractmethod


class Army:
    __metaclass__ = ABCMeta

    @abstractmethod
    def train_swordsman(self, name):
        pass

    @abstractmethod
    def train_lancer(self, name):
        pass

    @abstractmethod
    def train_archer(self, name):
        pass


class Warrior:
    def __init__(self, name, sub_type, army_type, basic_class):
        self.name = name
        self.sub_type = sub_type
        self.army_type = army_type
        self.basic_class = basic_class

    def introduce(self):
        return '{sub_type} {name}, {army_type} {basic_class}'.format(
            sub_type=self.sub_type, name=self.name,
            army_type=self.army_type, basic_class=self.basic_class)


class Swordsman(Warrior):
    def __init__(self, name, sub_type, army_type):
        super().__init__(name, sub_type, army_type, 'swordsman')


class Lancer(Warrior):
    def __init__(self, name, sub_type, army_type):
        super().__init__(name, sub_type, army_type, 'lancer')


class Archer(Warrior):
    def __init__(self, name, sub_type, army_type):
        super().__init__(name, sub_type, army_type, 'archer')


class AsianArmy(Army):
    def train_swordsman(self, name):
        return Swordsman(name, 'Samurai', 'Asian')

    def train_lancer(self, name):
        return Lancer(name, 'Ronin', 'Asian')

    def train_archer(self, name):
        return Archer(name, 'Shinobi', 'Asian')


class EuropeanArmy(Army):
    def train_swordsman(self, name):
        return Swordsman(name, 'Knight', 'European')

    def train_lancer(self, name):
        return Lancer(name, 'Raubritter', 'European')

    def train_archer(self, name):
        return Archer(name, 'Ranger', 'European')


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    my_army = EuropeanArmy()
    enemy_army = AsianArmy()

    soldier_1 = my_army.train_swordsman("Jaks")
    soldier_2 = my_army.train_lancer("Harold")
    soldier_3 = my_army.train_archer("Robin")

    soldier_4 = enemy_army.train_swordsman("Kishimoto")
    soldier_5 = enemy_army.train_lancer("Ayabusa")
    soldier_6 = enemy_army.train_archer("Kirigae")

    assert soldier_1.introduce() == "Knight Jaks, European swordsman"
    assert soldier_2.introduce() == "Raubritter Harold, European lancer"
    assert soldier_3.introduce() == "Ranger Robin, European archer"

    assert soldier_4.introduce() == "Samurai Kishimoto, Asian swordsman"
    assert soldier_5.introduce() == "Ronin Ayabusa, Asian lancer"
    assert soldier_6.introduce() == "Shinobi Kirigae, Asian archer"

    print("Coding complete? Let's try tests!")
