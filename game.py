from deck import Deck
from card import Card
from player import Player
import hand_evaluator
import random
import json
import copy
import asyncio

class Game(object):

    """Represents a game of texas holdem poker

    Attributes:
        max_table_size: 2-10
        round: integer 0-4
    """

    def __init__(self, **kwargs):
        self.id = 0
        self.max_table_size = kwargs["max_table_size"]
        self.table_name = kwargs["table_name"]
        self.players = kwargs["players"]
        self.deck = Deck()
        self.round = 0
        self.active_player = None
        self.board = [Card(0,0), Card(0,0), Card(0,0), Card(0,0), Card(0,0)]
        self.pot = 0
        self.highest_bet = 0
        self.blinds = kwargs["blinds"]
        self.quitting = False
        self.first_turn = False

    async def play(self):
        print("waiting for start conditions...")
        self.players.append(Player(id=0, name="Hans Hermann Hoppe", cash=10000, hand=[]))
        while (len(self.players) < 2):
            await asyncio.sleep(0.001)
        self.set_initial_positions()
        self.reset_game()
        while (self.quitting == False):
            while (self.is_end_of_round() == False and self.count_folded_players() < len(self.players)-1):
                if (self.first_turn == False):
                    self.set_active_player(self.next_active_player())
                else:
                    self.first_turn = False
                self.print_state()
                while(self.active_player.get_move(self) == False):
                    pass
            if (self.count_folded_players() == len(self.players) - 1):
                p = next(
                    player for player in self.players if player.has_folded == False)
                p.is_winner = True
                self.round = 4
                input("end of round*")
            self.next_round()
            if (self.round == 1):
                pass
            elif (self.round == 2):
                self.board[0] = self.deck.pop_card()
                self.board[1] = self.deck.pop_card()
                self.board[2] = self.deck.pop_card()
            elif (self.round == 3):
                self.board[3] = self.deck.pop_card()
            elif (self.round == 4):
                self.board[4] = self.deck.pop_card()
            elif (self.round == 0):
                self.set_active_player(None)
                winning_players = []
                for player in self.players:
                    if (player.is_winner == True):
                        winning_players.append(player)
                        break
                if (len(winning_players) > 0):
                    self.collect_pot(winning_players)
                    self.print_state()
                    input("end of round-by folding")
                else:
                    pos = 0
                    p = self.players[pos]
                    while (p.has_folded == True):
                        pos += 1
                        p = self.players[pos]
                    p1 = p
                    p2 = None
                    winners = [p1]
                    while (True):
                        pos += 1
                        if (pos != len(self.players)):
                            p = self.players[pos]
                        else: 
                            p = -1
                        while (p != -1 and p.has_folded == True):
                            pos += 1
                            if (pos != len(self.players)):
                                input("here: {}".format(p.name))
                                p = self.players[pos]
                            else:
                                p = -1
                        if (p == -1):
                            break
                        p2 = p
                        print("evaluating {} vs {}".format(p1.name, p2.name))
                        winner = hand_evaluator.winning_player(p1, p2, self.board)
                        if (winner == None):
                            print("winner is: DRAW")
                            winners.append(p2)
                        else:
                            print("winner is: {}".format(winner.name))
                            winners = [winner]
                            p1 = winner
                    for player in winners:
                        player.is_winner = True
                        print(winner.name)
                    self.collect_pot(winners)
                    self.print_state()
                    input("end of round- HERE")

    def collect_pot(self, winning_players):
        for player in winning_players:
            player.cash += self.pot/len(winning_players)
        self.pot = 0

    def quit(self):
        self.quitting = True

    def kick_broke_players(self):
        for player in self.players:
            if (player.cash == 0):
                player = None

    def count_folded_players(self):
        count = 0
        for player in self.players:
            if (player.has_folded == True):
                count += 1
        return count

    def next_round(self):
        print("going to next round")
        """if current round is 0, set to 1 (preflop), reset game, rotate positions,
            post blinds, and set third position player to active """
        if (self.round == 0):
            self.rotate_player_positions()
            self.reset_game()
        elif (self.round > 0 and self.round < 4):
            self.round += 1
            """set player to last nonfolded position (so when it increments you get the first)"""
            print("setting next player position(from next round method)")
            for i in range(0, len(self.players)):
                print(i)
                p = next(
                    player for player in self.players if player.position == i+1)
                if (p.has_folded == False):
                    print("next active player is {}".format(
                        self.active_player.name))
                    self.set_active_player(p)
                    print("setting active player to {}".format(p.name))
                    self.first_turn = True
                    break
        else:
            print(self.round)
            self.round = 0
        for player in self.players:
            player.bet_amount = 0
        self.highest_bet = 0

    def reset_game(self):
        print("resetting game")
        self.deck = Deck()
        self.deck.shuffle()
        for player in self.players:
            player.has_folded = False
            player.hand = []
            self.deck.move_cards(player.hand, 2)
            player.is_winner = False
        self.board = [Card(0,0), Card(0,0), Card(0,0), Card(0,0), Card(0,0)]
        self.round = 1
        self.pot = 0
        self.post_blinds()
        self.set_active_player(next(
            player for player in self.players if player.position == 2))

    def rotate_player_positions(self):
        for player in self.players:
            player.position -= 1
            if (player.position == 0):
                player.position = len(self.players)

    def is_end_of_round(self):
        print("checking for end of round...")
        bb = self.get_bb()
        sb = self.get_sb()
        if(self.round == 1):
            bb.position += self.max_table_size
            sb.position += self.max_table_size
        for player in self.players:
            if (player.has_folded == False and (player.bet_amount != self.highest_bet or player.position > self.active_player.position)):
                print(
                    "found continuation condition for {}: player.bet_amount != self.highest_bet is {}; player.position > self.active_player.position is {}".format(player.name, player.bet_amount != self.highest_bet, player.position > self.active_player.position))
                if(self.round == 1):
                    bb.position -= self.max_table_size
                    sb.position -= self.max_table_size
                print("returning False")
                return False
        if(self.round == 1):
            bb.position -= self.max_table_size
            sb.position -= self.max_table_size
        print("returning True")
        return True

    def next_active_player(self):
        print("setting next active player")
        for i in range(self.active_player_index(), len(self.players)):
            if (self.players[i].has_folded == False and self.players[i] != self.active_player):
                return self.players[i]
        for i in range(0, self.active_player_index()):
            if (self.players[i].has_folded == False):
                return self.players[i]
        return None

    def set_active_player(self, player):
        print("setting active player")
        if (self.active_player != None):
            #print("current active player:{}".format(self.active_player.name))
            self.active_player.is_active = False
        #print("new active player: {}".format(player.name))
        if (player != None):
            player.is_active = True
        self.active_player = player

    def active_player_index(self):
        for i in range(0, len(self.players)):
            if (self.players[i].is_active == True):
                return i
        return -1

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

    def get_bb(self):
        return next(player for player in self.players if player.position == 2)

    def get_sb(self):
        return next(player for player in self.players if player.position == 1)

    def post_blinds(self):
        self.get_sb().bet(self.blinds[0], self) + \
            self.get_bb().bet(self.blinds[1], self)

    def print_state(self):
        """prints a representation of the game state"""
        rounds = ["End", "Preflop", "Flop", "Turn", "River"]
        state = rounds[self.round] + "\n" + "-" * 7 + "\n" + "Board: {}\n".format(
            self.board) + "Pot: {}\n".format(self.pot) + "-" * 7 + "\n"
        indices = []
        """player names"""
        line = "Player: "
        for player in self.players:
            if (player.is_winner == True):
                line += "WINNER" + " " * 3
            elif (player.is_active == True):
                line += "*" + player.name + " " * 6
            else:
                line += player.name + " " * 7
            indices.append(len(line))
        state += line + "\n"
        """player positions"""
        line = "Pos:    "
        for i in range(len(self.players)):
            line += str(self.players[i].position)
            while (len(line) < indices[i]):
                line += " "
        state += line + "\n"
        """player hands"""
        line = "Hand:   "
        for i in range(len(self.players)):
            if (self.players[i].has_folded == False):
                line += str(self.players[i].hand)
            else:
                line += "FOLD"
            while (len(line) < indices[i]):
                line += " "
        state += line + "\n"
        """player cash"""
        line = "Cash:   "
        for i in range(len(self.players)):
            line += str(self.players[i].cash)
            while (len(line) < indices[i]):
                line += " "
        state += line + "\n"
        """player bets"""
        line = "Bet:    "
        for i in range(len(self.players)):
            line += str(self.players[i].bet_amount)
            while (len(line) < indices[i]):
                line += " "
        state += line
        """decorate"""
        state = "_" * indices[len(indices)-1] + "\n" + \
            state + "\n" + "_" * indices[len(indices)-1]
        print(state)

    def asdict(self):

        player_list = []
        deck_list = []
        board_list = []

        for player in self.players:
            player_list.append(player.asdict())
        for card in self.deck.cards:
            deck_list.append(card.asdict())
        for card in self.board:
            board_list.append(card.asdict())
        active_p = None
        if (self.active_player != None):
            active_p = self.active_player.asdict()
        return {'id' : self.id,
            'max_table_size' : self.max_table_size,
            'table_name': self.table_name,
            'players' : player_list,
            'deck' : deck_list,
            'round' : self.round,
            'active_player' : active_p,
            'board' : board_list,
            'pot' : self.pot,
            'highest_bet' : self.highest_bet,
            'blinds' : self.blinds}