from game import Game
from player import Player


def main():

    players = []
    for i in range(0, 6):
        players.append(Player(name="P{}".format(i+1), cash=10000, hand=[]))
    Game(id=0, max_table_size=6, table_name="test",
         players=players, blinds=[100, 200])


if __name__ == "__main__":
    main()
