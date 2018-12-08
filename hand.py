from card import Card
from deck import Deck
import json


class Hand(Deck):
    def __init__(self, label=''):
        self.cards = []
        self.label = label

    def asdict(self):
        return json.dumps(card.__dict__ for card in self.cards)
