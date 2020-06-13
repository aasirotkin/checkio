class VoiceCommand:
    def __init__(self, channels: tuple):
        self.cur_channel = 0
        self.channels = channels

    @property
    def length(self):
        return len(self.channels)

    def exist(self, name_or_number) -> bool:
        if type(name_or_number) == str:
            return name_or_number in self.channels
        else:
            return 1 <= name_or_number <= self.length

    def is_exist(self, name_or_number) -> str:
        return 'Yes' if self.exist(name_or_number) else 'No'

    def turn_channel(self, channel: int) -> str:
        self.cur_channel = channel - 1
        if self.cur_channel >= self.length:
            self.cur_channel = 0
        elif self.cur_channel < 0:
            self.cur_channel = self.length - 1
        return self.channels[self.cur_channel]

    def first_channel(self) -> str:
        return self.turn_channel(1)

    def last_channel(self) -> str:
        return self.turn_channel(self.length)

    def previous_channel(self) -> str:
        return self.turn_channel(self.cur_channel)

    def current_channel(self):
        return self.turn_channel(self.cur_channel + 1)

    def next_channel(self) -> str:
        return self.turn_channel(self.cur_channel + 2)


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    CHANNELS = ["BBC", "Discovery", "TV1000"]

    controller = VoiceCommand(CHANNELS)

    assert controller.first_channel() == "BBC"
    assert controller.last_channel() == "TV1000"
    assert controller.turn_channel(1) == "BBC"
    assert controller.next_channel() == "Discovery"
    assert controller.previous_channel() == "BBC"
    assert controller.current_channel() == "BBC"
    assert controller.is_exist(4) == "No"
    assert controller.is_exist("TV1000") == "Yes"
    print("Coding complete? Let's try tests!")
