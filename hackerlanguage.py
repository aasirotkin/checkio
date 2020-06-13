from re import match as re_match


class HackerLanguage:
    special = {'.', ':', '!', '?', '@', '$', '%'}
    whitespace = '1000000'
    date_format = '\\d\\d\\.\\d\\d\\.\\d\\d\\d\\d'
    time_format = '\\d\\d:\\d\\d'

    @staticmethod
    def bin_converter(x: str, encrypt: bool) -> str:
        return format(ord(x), 'b') if encrypt else chr(int(x, 2))

    @staticmethod
    def match(msg: str) -> 0:
        rm = re_match(HackerLanguage.date_format, msg)
        if rm:
            return rm.span()[1]
        rm = re_match(HackerLanguage.time_format, msg)
        if rm:
            return rm.span()[1]
        return 0

    def __init__(self): self.msg = ''

    def write(self, msg): self.msg += msg

    def delete(self, number): self.msg = self.msg[:-number]

    def is_my_space(self, msg: str, encrypt: bool) -> bool:
        if encrypt:
            return msg[0].isspace()
        else:
            return msg.startswith(self.whitespace)

    def encr_decr(self, msg: str, encrypt: bool = True):
        encrypted = ''
        i, length = 0, len(msg)
        size = 1 if encrypt else 7
        while i != length:
            part, symbol = msg[i:], msg[i:i+size]
            shift = self.match(part)
            if shift:
                encrypted += part[0:shift]
            elif symbol[0] in self.special:
                encrypted += symbol[0]
                i -= (size - 1)
            elif self.is_my_space(part, encrypt):
                encrypted += ' ' if not encrypt else self.whitespace
            else:
                encrypted += self.bin_converter(symbol, encrypt)
            i += max(size, shift)
        return encrypted

    def read(self, msg) -> str:
        return self.encr_decr(msg, False)

    def send(self) -> str:
        return self.encr_decr(self.msg)


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    message_1 = HackerLanguage()
    message_1.write("secrit")
    message_1.delete(2)
    message_1.write("et")
    message_2 = HackerLanguage()

    assert message_1.send() == "111001111001011100011111001011001011110100"
    assert message_2.read("11001011101101110000111010011101100") == "email"

    message_3 = HackerLanguage()
    message_3.write('Remember: 21.07.2018 at 11:11AM')
    message_3.delete(2)
    message_3.write('PM')
    assert message_3.send() == '10100101100101110110111001011101101110001011001011110010:100000021.07.2018100000011000011110100100000011:1110100001001101'

    message_4 = HackerLanguage()
    assert message_4.read('10011011111001100000011001011101101110000111010011101100100000011010011110011100000011011011110010.11100101101111110001011011111110100@11001111101101110000111010011101100.110001111011111101101') == 'My email is mr.robot@gmail.com'

    assert message_1.send() == "111001111001011100011111001011001011110100"
    assert message_2.read("11001011101101110000111010011101100") == "email"
    print("Coding complete? Let's try tests!")
