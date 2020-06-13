class MicrowaveBase:
    def __init__(self):
        self.time = 0

    def add_seconds(self, seconds: int) -> None:
        self.time = min(5400, self.time + seconds)

    def del_seconds(self, seconds: int) -> None:
        self.time = max(0, self.time - seconds)

    def set_seconds(self, seconds: int) -> None:
        self.time = seconds if 0 <= seconds <= 5400 else 0 if seconds < 0 else 5400

    @property
    def minuets(self): return int(self.time/60)

    @property
    def seconds(self): return self.time - 60*self.minuets

    def show(self) -> str:
        return '{:02d}:{:02d}'.format(self.minuets, self.seconds)


class Microwave1(MicrowaveBase):
    def show(self) -> str:
        return '_{:01d}:{:02d}'.format(self.minuets % 10, self.seconds)


class Microwave2(MicrowaveBase):
    def show(self) -> str:
        return '{:02d}:{:01d}_'.format(self.minuets, self.seconds // 10)


class Microwave3(MicrowaveBase):
    pass


class RemoteControl:
    def __init__(self, micro: MicrowaveBase):
        self.micro = micro

    def set_time(self, time: str) -> None:
        m, s = map(int, time.split(sep=':'))
        self.micro.add_seconds(m*60+s)

    @staticmethod
    def to_seconds(time: str) -> int:
        if time.endswith('s'):
            return int(time[:-1])
        else:
            return int(time[:-1])*60

    def add_time(self, time: str) -> None:
        self.micro.add_seconds(self.to_seconds(time))

    def del_time(self, time: str) -> None:
        self.micro.del_seconds(self.to_seconds(time))

    def show_time(self) -> str:
        return self.micro.show()


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    microwave_1 = Microwave1()
    microwave_2 = Microwave2()
    microwave_3 = Microwave3()

    remote_control_1 = RemoteControl(microwave_1)
    remote_control_1.set_time("01:00")

    remote_control_2 = RemoteControl(microwave_2)
    remote_control_2.add_time("90s")

    remote_control_3 = RemoteControl(microwave_3)
    remote_control_3.del_time("300s")
    remote_control_3.add_time("100s")

    assert remote_control_1.show_time() == "_1:00"
    assert remote_control_2.show_time() == "01:3_"
    assert remote_control_3.show_time() == "01:40"
    print("Coding complete? Let's try tests!")
