from hand import Hand


class Player(object):

    def __init__(self, name, cash):
        self.name = name
        self.cash = cash
        self.hand = Hand("{}\'s hand".format(name))
        self.position = -1
        self.isActive = False

    def bet(self, amount):
        self.cash -= amount
        return amount

    def asdict(self):
        return {'name': self.name,
                'cash': self.cash,
                'hand': self.hand.asdict(),
                'position': self.position,
                'isActive': self.isActive}
