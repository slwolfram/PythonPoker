from deck import Deck
from player import Player
import random
import json


class Game(object):

    states = ["None", "Preflop", "Flop", "Turn", "River"]

    def __init__(self, max_table_size, players, blinds):
        self.max_table_size = max_table_size
        self.players = players
        self.deck = Deck()
        self.state = self.states[0]
        self.active_player = None
        self.board = ["", "", "", "", ""]
        self.pot = 0
        self.blinds = blinds

    def start(self):
        self.deck.shuffle
        for player in self.players:
            self.deck.move_cards(player.hand, 2)

        self.set_initial_positions()

        self.state = self.state[1]

        self.post_blinds()

        while (self.state == "Preflop"):
            pass

    def set_initial_positions(self):
        """set player positions"""
        """positions start at 1"""
        start = random.randint(0, len(self.players))
        position = 1
        for i in range(start, len(self.players)):
            self.players[i].position = position
            position += 1
        for i in range(start):
            self.players[i].position = position
            position += 1

    def get_json_state(self):
        return json.dumps(player.__dict__ for player in self.players)

    def get_bb(self):
        return next(player for player in self.players if player.position == 0)

    def get_sb(self):
        return next(player for player in self.players if player.position == 1)

    def post_blinds(self):
        self.pot += self.get_bb().bet(self.blinds[1]) + \
            self.get_sb().bet(self.blinds[0])
