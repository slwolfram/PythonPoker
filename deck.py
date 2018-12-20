from card import Card
import random


class Deck(object):
    """Represents a deck of cards

    Attributes: 
      cards: list of Card objects
    """

    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return ','.join(res)

    def add_card(self, card):
        """Adds a card to the deck"""
        self.cards.append(card)

    def remove_card(self, card):
        """Removes a card from the deck"""
        self.cards.remove(card)

    def pop_card(self, i=-1):
        """Removes and returns a card from the deck"""
        """i: index of the card to draw, the last by default"""
        return self.cards.pop(i)

    def shuffle(self):
        random.shuffle(self.cards)

    def sort(self):
        """sorts the cards in ascending order."""
        self.cards.sort()

    def move_cards(self, hand, num):
        """Moves the given number of cards from the deck into the Hand.:"""
        for i in range(num):
            hand.append(self.pop_card())
