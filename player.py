import json
from card import Card


class Player(object):

    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.cash = 10000
        self.hand = [Card(0, 0), Card(0, 0)]
        self.position = -1
        self.bet_amount = 0
        self.is_active = False
        self.has_folded = False
        self.is_winner = False

    def get_move(self, game):
        """asks for player input"""
        """returns false if the move has not executed successfully"""
        move = input("{}\'s turn:".format(self.name)).lower().split()
        if (move == None or len(move) == 0):
            print("Invalid input: None")
            return False
        if (move[0] == "fold"):
            return self.fold(game)
        if (move[0] == "bet" and len(move) > 1 and int(move[1]) > 0):
            return self.bet(int(move[1]), game)
        if (move[0] == "call" or move[0] == "check"):
            return self.check_call(game)
        print("Invalid input: syntax error")
        return False

    def fold(self, game):
        if (self.bet_amount == game.highest_bet):
            print("You can't fold if you can check.")
            return False
        print("{} folds.".format(self.name))
        self.has_folded = True
        return True

    def bet(self, amount, game):
        if (amount + self.bet_amount >= game.highest_bet):
            if (amount + self.bet_amount == game.highest_bet):
                print("{} calls for ${}".format(self.name, amount))
            else:
                print("{} bets ${}".format(self.name, amount))
            self.cash -= amount
            self.bet_amount += amount
            game.highest_bet = self.bet_amount
            game.pot += amount
            return True
        else:
            print("Invalid bet amount: {}".format(amount))
            return False

    def check_call(self, game):
        if (self.bet_amount == game.highest_bet):
            print("{} checks".format(self.name))
            return True
        else:
            call_value = game.highest_bet - self.bet_amount
            self.bet(call_value, game)
            return True

    def __str__(self):
        return "name:{} cash:{} hand:{},{} position:{}".format(self.name, self.cash, self.hand[0], self.hand[1], self.position)

    def asdict(self):

        hand_list = []
        for card in self.hand:
            hand_list.append(card.asdict)

        return {
            'id': self.id,
            'name': self.name,
            'cash': self.cash,
            'hand': hand_list,
            'position': self.position,
            'bet_amount': self.bet_amount,
            'is_active': self.is_active,
            'has_folded': self.has_folded,
            'is_winner': self.is_winner
        }
