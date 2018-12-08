class Card(object):
    """Represents a standard playing card

    Attributes:
        suit: integer 0-3
        rank: integer 1-13
    """

    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = ["None", "Ace", "2", "3", "4", "5", "6",
                  "7", "8", "9", '10', "Jack", "Queen", "King"]

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """Returns a human-readable string representation"""
        return "%s of %s" % (Card.suit_names[self.suit], Card.rank_names[self.rank])
