from player import Player
from card import Card
import hand_evaluator


def main():
    print("testing hand evaluator for:")
    p1 = Player(name="P1", cash="1000", hand=[Card(1, 1), Card(2, 1)])
    p2 = Player(name="P2", cash="1000", hand=[Card(1, 3), Card(2, 4)])
    board = [Card(1, 2), Card(2, 3), Card(2, 3), Card(3, 4), Card(3, 9)]
    winner = hand_evaluator.winning_player(p1, p2, board)
    print(str(winner))


if __name__ == "__main__":
    main()
