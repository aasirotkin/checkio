class Text:
    def __init__(self):
        self.text = ''
        self.font = ''

    def write(self, text: str) -> None:
        self.text += text

    def set_font(self, font: str) -> None:
        self.font = '[{}]'.format(font)

    def show(self) -> str:
        return '{font}{text}{font}'.format(font=self.font, text=self.text)

    def restore(self, restored: tuple) -> None:
        self.font = restored[0]
        self.text = restored[1]


class SavedText:
    def __init__(self):
        self.saved = []

    def save_text(self, text: Text) -> None:
        self.saved.append((text.font, text.text))

    @property
    def versions_amount(self):
        return len(self.saved)

    def get_version(self, version: int) -> tuple:
        return self.saved[version] if version < self.versions_amount else ''


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    text = Text()
    saver = SavedText()

    text.write("At the very beginning ")
    saver.save_text(text)
    text.set_font("Arial")
    saver.save_text(text)
    text.write("there was nothing.")

    assert text.show() == "[Arial]At the very beginning there was nothing.[Arial]"

    text.restore(saver.get_version(0))
    assert text.show() == "At the very beginning "

    print("Coding complete? Let's try tests!")
