class Card(object):
    """Represents a standard playing card

    Attributes:
        suit: integer 0-3
        rank: integer 1-13
    """

    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = ["None", "Ace", "2", "3", "4", "5", "6",
                  "7", "8", "9", '10', "Jack", "Queen", "King", "Ace"]

    short_suit_names = ["c", "d", "h", "s"]
    short_rank_names = ["0", "A", "2", "3", "4",
                        "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self, suit, rank):
        self.rank = rank
        self.suit = suit

    # def __str__(self):
    #    """Returns a human-readable string representation"""
    #    return "%s of %s" % (Card.suit_names[self.suit], Card.rank_names[self.rank])

    def __str__(self):
        if (self.rank == 0):
            return "XX"
        return Card.short_rank_names[self.rank] + Card.short_suit_names[self.suit]

    def __repr__(self):
        return str(self)

    def asdict(self):
        return {'suit': self.suit, 'rank': self.rank}
