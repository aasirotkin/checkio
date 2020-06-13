class Weapon:
    def __init__(self, health: int = 0, attack: int = 0,
                 defense: int = 0, vampirism: int = 0, heal_power: int = 0):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.vampirism = vampirism
        self.heal_power = heal_power


class Sword(Weapon):
    def __init__(self):
        super().__init__(health=5, attack=2)


class Shield(Weapon):
    def __init__(self):
        super().__init__(health=20, attack=-1, defense=2)


class GreatAxe(Weapon):
    def __init__(self):
        super().__init__(health=-15, attack=5, defense=-2, vampirism=10)


class Katana(Weapon):
    def __init__(self):
        super().__init__(health=-20, attack=6, defense=-5, vampirism=50)


class MagicWand(Weapon):
    def __init__(self):
        super().__init__(health=30, attack=3, heal_power=3)


class Warrior:
    def __init__(self, health: int = 50, attack: int = 5, defense: int = 0,
                 vampirism: int = 0, extra_attack: int = 0, heal_power: int = 0):
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.vampirism = vampirism
        self.extra_attack = extra_attack
        self.heal_power = heal_power

    @property
    def is_alive(self):
        return self.health > 0

    def first_hit(self, enemy):
        self.hit(enemy, self.attack)

    def second_hit(self, enemy):
        self.hit(enemy, self.attack*(self.extra_attack/100.0))

    def hit(self, enemy, attack):
        if enemy.defense < attack:
            dealt_damage = attack - enemy.defense
            enemy.health -= dealt_damage
            self.health = min(self.health + int(dealt_damage*(self.vampirism/100.0)),
                              self.max_health)

    def equip_weapon(self, weapon):
        self.health = max(self.health + weapon.health, 0)
        self.max_health = self.health
        self.attack = max(self.attack + weapon.attack, 0) if self.attack > 0 else 0
        self.defense = max(self.defense + weapon.defense, 0) if self.defense > 0 else 0
        self.vampirism = max(self.vampirism + weapon.vampirism, 0) if self.vampirism > 0 else 0
        self.heal_power = max(self.heal_power + weapon.heal_power, 0) if self.heal_power > 0 else 0


class Healer(Warrior):
    def __init__(self, health: int = 60, attack: int = 0, heal_power: int = 2):
        super().__init__(health=health, attack=attack, heal_power=heal_power)

    def heal(self, ally):
        ally.health = min(ally.max_health, ally.health + self.heal_power)


class Lancer(Warrior):
    def __init__(self, health: int = 50, attack: int = 6, extra_attack: int = 50):
        super().__init__(health=health, attack=attack, extra_attack=extra_attack)


class Vampire(Warrior):
    def __init__(self, health: int = 40, attack: int = 4, vampirism: int = 50):
        super().__init__(health=health, attack=attack, vampirism=vampirism)


class Knight(Warrior):
    def __init__(self, health: int = 50, attack: int = 7):
        super().__init__(health, attack)


class Defender(Warrior):
    def __init__(self, health: int = 60, attack: int = 3, defense: int = 2):
        super().__init__(health, attack, defense)


class Rookie(Warrior):
    def __init__(self, health: int = 50, attack: int = 1):
        super().__init__(health, attack)


class Warlord(Warrior):
    def __init__(self, health: int = 100, attack: int = 4, defense: int = 2):
        super().__init__(health=health, attack=attack, defense=defense)


class Army:
    def __init__(self):
        self.units = list()

    def move_units(self):
        if not self.is_warlord_here:
            return
        self.units.sort(key=lambda i: type(i) == Lancer, reverse=True)
        self.units.sort(key=lambda i: i.attack > 0, reverse=True)
        self.units.sort(key=lambda i: type(i) != Warlord, reverse=True)
        for u, unit in enumerate(self.units):
            if type(unit) == Healer and u > 1:
                self.units.insert(1, self.units.pop(u))

    @property
    def is_warlord_here(self) -> bool:
        return any(type(unit) == Warlord for unit in self.units)

    def add_units(self, unit_type, amount: int) -> None:
        if unit_type == Warlord:
            if self.is_warlord_here:
                amount = 0
            else:
                amount = 1
        for unit in range(amount):
            self.units.append(unit_type())

    def is_union_dead(self, unit: int) -> bool:
        if self.length > unit and \
                not self.units[unit].is_alive:
            del self.units[unit]
            self.is_union_dead(unit+1)
            self.move_units()
            return True
        return False

    def hit(self, enemy_arms, unit: int = 0) -> bool:
        next_unit = unit+1
        self.units[unit].first_hit(enemy_arms.units[unit])
        if enemy_arms.length > next_unit:
            if type(self.units[unit]) == Lancer:
                self.units[unit].second_hit(enemy_arms.units[next_unit])
        if self.length > next_unit:
            if type(self.units[next_unit]) == Healer:
                self.units[next_unit].heal(self.units[unit])
        return enemy_arms.is_union_dead(unit)

    def remove_units(self, units: list):
        for unit in sorted(units, reverse=True):
            del self.units[unit]

    @property
    def is_alive(self) -> bool:
        return self.length > 0

    @property
    def length(self) -> int:
        return len(self.units)


class Battle:
    @staticmethod
    def fight(army_1: Army, army_2: Army) -> bool:
        step = 0
        while army_1.is_alive and army_2.is_alive:
            if step % 2 == 0:
                if army_1.hit(army_2):
                    step += 1
            else:
                army_2.hit(army_1)
            step += 1

        return army_1.is_alive

    @staticmethod
    def alone_fight(unit_1, unit_2):
        step = 0
        while unit_1.is_alive and unit_2.is_alive:
            if step % 2 == 0:
                unit_1.first_hit(unit_2)
            else:
                unit_2.first_hit(unit_1)
            step += 1

        return unit_1.is_alive

    @staticmethod
    def straight_fight(army_1: Army, army_2: Army) -> bool:
        step = 0
        while army_1.is_alive and army_2.is_alive:
            death = [(unit, not Battle.alone_fight(army_1.units[unit], army_2.units[unit]))
                     for unit in range(min(army_1.length, army_2.length))]
            army_1.remove_units([unit for unit, dead in death if dead])
            army_2.remove_units([unit for unit, dead in death if not dead])
        return army_1.is_alive


def fight(unit_1, unit_2):
    step = 0
    while unit_1.is_alive and unit_2.is_alive:
        if step % 2 == 0:
            unit_1.first_hit(unit_2)
        else:
            unit_2.first_hit(unit_1)
        step += 1

    return unit_1.is_alive


if __name__ == '__main__':
    ronald = Warlord()
    heimdall = Knight()

    fight(heimdall, ronald) == False

    my_army = Army()
    my_army.add_units(Warlord, 1)
    my_army.add_units(Warrior, 2)
    my_army.add_units(Lancer, 2)
    my_army.add_units(Healer, 2)

    enemy_army = Army()
    enemy_army.add_units(Warlord, 3)
    enemy_army.add_units(Vampire, 1)
    enemy_army.add_units(Healer, 2)
    enemy_army.add_units(Knight, 2)

    my_army.move_units()
    enemy_army.move_units()

    type(my_army.units[0]) == Lancer
    type(my_army.units[1]) == Healer
    type(my_army.units[-1]) == Warlord

    type(enemy_army.units[0]) == Vampire
    type(enemy_army.units[-1]) == Warlord
    type(enemy_army.units[-2]) == Knight

    # 6, not 8, because only 1 Warlord per army could be
    len(enemy_army.units) == 6

    battle = Battle()

    battle.fight(my_army, enemy_army) == True
    print("Coding complete? Let's try tests!")
