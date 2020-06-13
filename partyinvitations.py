class Friend:
    def __init__(self, name: str):
        self.name = name
        self.parties = ['No party...']

    def add_invitation(self, place: str, time: str) -> None:
        self.parties.append('{}: {}'.format(place, time))

    def show_invite(self) -> str:
        return self.parties[-1]


class Party:
    def __init__(self, place: str):
        self.place = place
        self.friends = set()

    def add_friend(self, friend: Friend) -> None:
        self.friends.add(friend)

    def del_friend(self, friend: Friend) -> None:
        if friend in self.friends:
            self.friends.remove(friend)

    def send_invites(self, time: str) -> None:
        for friend in self.friends:
            friend.add_invitation(self.place, time)


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    party = Party("Midnight Pub")
    nick = Friend("Nick")
    john = Friend("John")
    lucy = Friend("Lucy")
    chuck = Friend("Chuck")

    party.add_friend(nick)
    party.add_friend(john)
    party.add_friend(lucy)
    party.send_invites("Friday, 9:00 PM")
    party.del_friend(nick)
    party.send_invites("Saturday, 10:00 AM")
    party.add_friend(chuck)

    assert john.show_invite() == "Midnight Pub: Saturday, 10:00 AM"
    assert lucy.show_invite() == "Midnight Pub: Saturday, 10:00 AM"
    assert nick.show_invite() == "Midnight Pub: Friday, 9:00 PM"
    assert chuck.show_invite() == "No party..."
    print("Coding complete? Let's try tests!")
