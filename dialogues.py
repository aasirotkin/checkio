VOWELS = "aeiou"


class Person:
    def __init__(self, name: str, is_human: bool) -> None:
        self.name = name
        self.is_human = is_human
        self.chat = None

    def send(self, msg: str) -> bool:
        if self.chat:
            self.chat.append(self.name, msg)
            return True
        return False

    def set_chat(self, chat) -> None:
        self.chat = chat


class Chat:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.conversation = list()
            cls.instance = super(Chat, cls).__new__(cls)
        return cls.instance

    def connect_human(self, human):
        human.set_chat(self)

    def connect_robot(self, robot):
        robot.set_chat(self)

    def append(self, name: str, msg: str):
        self.conversation.append((name, msg))

    @staticmethod
    def convert(msg: str) -> str:
        return ''.join('1' if s.lower() not in VOWELS else '0'
                       for s in msg)

    def show_human_dialogue(self):
        return '\n'.join(f'{name} said: {phrase}'
                         for name, phrase in self.conversation)

    def show_robot_dialogue(self):
        return '\n'.join(f'{name} said: {self.convert(phrase)}'
                         for name, phrase in self.conversation)


class Human(Person):
    def __init__(self, name):
        super().__init__(name, True)


class Robot(Person):
    def __init__(self, name):
        super().__init__(name, False)


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    chat = Chat()
    karl = Human("Karl")
    bot = Robot("R2D2")
    chat.connect_human(karl)
    chat.connect_robot(bot)
    karl.send("Hi! What's new?")
    bot.send("Hello, human. Could we speak later about it?")
    assert chat.show_human_dialogue() == """Karl said: Hi! What's new?
R2D2 said: Hello, human. Could we speak later about it?"""
    assert chat.show_robot_dialogue() == """Karl said: 101111011111011
R2D2 said: 10110111010111100111101110011101011010011011"""

    print("Coding complete? Let's try tests!")
