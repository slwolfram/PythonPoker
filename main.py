from game import Game
from player import Player


def main():

    players = []
    for i in range(0, 6):
        players.append(Player("Player {}".format(i), 10000))
    Game(6, players, [500, 1000])


if __name__ == "__main__":
    main()
