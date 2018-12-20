import copy
import functools
from card import Card


def _log_function(func):
    def wrapper(*args, **kwargs):
        print("starting {}".format(func.__name__))
        value = func(*args, **kwargs)
        print("ending {}".format(func.__name__))
        return value
    return wrapper

@_log_function
def winning_player(player_1, player_2, board):
    top_hand_1 = top_hand(player_1.hand, board)
    top_hand_2 = top_hand(player_2.hand, board)

    print(top_hand_1["hand_ranking"])
    print(top_hand_2["hand_ranking"])
    #input("printing hand results")
    
    """compare hand_rankings"""
    if (top_hand_1["hand_ranking"] < top_hand_2["hand_ranking"]):
        return player_1
    elif (top_hand_1["hand_ranking"] > top_hand_2["hand_ranking"]):
        return player_2
    elif (top_hand_1["hand_ranking"] == 1):
        """if both players have straight flush"""
        if (top_hand_1["top_cards"][0].rank > top_hand_2["top_cards"][0].rank):
            return player_1
        elif (top_hand_1["top_cards"][0].rank < top_hand_2["top_cards"][0].rank):
            return player_2
        print("draw. Players have equivalent straight flush")
        return None
    elif (top_hand_1["hand_ranking"] == 2):
        """if both players have four of a kind"""
        if (top_hand_1["top_cards"][0].rank > top_hand_2["top_cards"][0].rank):
            return player_1
        elif (top_hand_1["top_cards"][0].rank < top_hand_2["top_cards"][0].rank):
            return player_2
    elif (top_hand_1["hand_ranking"] == 3):
        """if both players have full house"""
        if (top_hand_1["top_cards"][0].rank > top_hand_2["top_cards"][0].rank):
            return player_1
        elif (top_hand_1["top_cards"][0].rank < top_hand_2["top_cards"][0].rank):
            return player_2
        elif (top_hand_1["top_cards"][-1].rank > top_hand_2["top_cards"][-1].rank):
            return player_1
        elif (top_hand_1["top_cards"][-1].rank < top_hand_2["top_cards"][-1].rank):
            return player_2
        print("draw. Players have equivalent full house")
        return None
    elif (top_hand_1["hand_ranking"] == 4):
        """compare flushes for high card"""
        for i in range(len(top_hand_1) - 1, -1):
            if (top_hand_1["top_hand"][i] > top_hand_2["top_hand"][i]):
                return player_1
            elif (top_hand_1["top_hand"][i] < top_hand_2["top_hand"][i]):
                return player_2
        return None
    elif (top_hand_1["hand_ranking"] == 5):
        """if both players have straight"""
        if (top_hand_1["top_cards"][0].rank > top_hand_2["top_cards"][0].rank):
            return player_1
        elif (top_hand_1["top_cards"][0].rank < top_hand_2["top_cards"][0].rank):
            return player_2
        print("draw. Players have equivalent straight")
        return None
    elif (top_hand_1["hand_ranking"] == 6):
        """if both player have three of a kind"""
        if (top_hand_1["top_cards"][0].rank > top_hand_2["top_cards"][0].rank):
            return player_1
        elif (top_hand_1["top_cards"][0].rank < top_hand_2["top_cards"][0].rank):
            return player_2
        for i in range(3, len(top_hand_1["top_hand"])):
            if (top_hand_1["top_hand"][i] > top_hand_2["top_hand"][i]):
                return player_1
            elif (top_hand_1["top_hand"][i] < top_hand_2["top_hand"][i]):
                return player_2
        print("draw. Players have equivalent three of a kind")
        return None
    elif (top_hand_1["hand_ranking"] == 7):
        """if both players have two pair"""
        if (top_hand_1["top_cards"][0].rank > top_hand_2["top_cards"][0].rank):
            return player_1
        elif (top_hand_1["top_cards"][0].rank < top_hand_2["top_cards"][0].rank):
            return player_2
        elif (top_hand_1["top_cards"][2].rank > top_hand_2["top_cards"][2].rank):
            return player_1
        elif (top_hand_1["top_cards"][2].rank < top_hand_2["top_cards"][2].rank):
            return player_2
        elif (top_hand_1["top_cards"][-1].rank > top_hand_2["top_cards"][-1].rank):
            return player_1
        elif (top_hand_1["top_cards"][-1].rank < top_hand_2["top_cards"][-1].rank):
            return player_2
        print("draw. Players have equivalent two pair")
        return None
    elif (top_hand_1["hand_ranking"] == 8):
        """if both player have two of a kind"""
        if (top_hand_1["top_cards"][0].rank > top_hand_2["top_cards"][0].rank):
            return player_1
        elif (top_hand_1["top_cards"][0].rank < top_hand_2["top_cards"][0].rank):
            return player_2
        for i in range(2, len(top_hand_1["top_hand"])):
            """compare the rest of the cards for high card"""
            if (top_hand_1["top_hand"][i].rank > top_hand_2["top_hand"][i].rank):
                return player_1
            elif (top_hand_1["top_hand"][i].rank < top_hand_2["top_hand"][i].rank):
                return player_2
        print("draw. Players have equivalent two of a kind")
        return None
    for i in range(4, -1):
        if (top_hand_1["top_hand"][i].rank > top_hand_2["top_hand"][i].rank):
            return player_1
        elif (top_hand_1["top_hand"][i].rank < top_hand_2["top_hand"][i].rank):
            return player_2
    print("draw. Players have the same hand")
    return None
        
@_log_function
def top_hand(hand, board):
    result = straight_flush(hand, board)
    if (result != None):
        #input("returning straight flush")
        return result
    result = four_of_a_kind(hand, board)
    if (result != None):
        #input("returning four of a kind")
        return result
    result = full_house(hand, board)
    if (result != None):
        #input("returning full house")
        return result
    result = flush(hand, board)
    if (result != None):
        #input("returning flush")
        return result
    result = straight(hand, board)
    if (result != None):
        #input("returning straight")
        return result
    result = three_of_a_kind(hand, board)
    if (result != None):
        #input("returning three of a kind")
        return result
    result = two_pair(hand, board)
    if (result != None):
        return result
    result = two_of_a_kind(hand, board)
    if (result != None):
        #input("returning two of a kind")
        return result
    else:
        #input("returning high card")
        return high_card(hand, board)

@_log_function
def straight_flush(hand, board):
    fl = get_flush_cards(hand, board)
    if (fl != None):
        print(fl)
        #input("got flush, starting straight check")
        result = straight(fl, [])
        if (result != None):
            return {"hand_ranking": 1,
                    "top_cards": result["top_cards"],
                    "top_hand": result["top_hand"]}
    return None

@_log_function
def four_of_a_kind(hand, board):
    cards = prep_cards(hand, board)
    i = len(cards) - 1
    for card in cards:
        print(str(card) + " rank: " + str(card.rank))
    while (i - 3 >= 0):
        if (cards[i].rank == cards[i-1].rank
                == cards[i-2].rank == cards[i-3].rank):
            top_cards = [cards[i], cards[i-1], cards[i-2], cards[i-3]]
            top_hand = top_cards.append(cards[-1]) if cards[-1] > i else top_cards.append(cards[i-4])
            return {"hand_ranking": 2,
                    "top_cards": top_cards,
                    "top_hand": top_hand}
        i -=1
    return None

@_log_function
def full_house(hand, board):
    #input("in full house")
    result = three_of_a_kind(hand, board)
    print("hand:")
    for card in hand:
        print(str(card))
    for card in board:
        print(str(card))
    #input("got result")
    if (result != None):
        #input("has three of a kind")
        cards = prep_cards(hand, board)
        for card in result["top_cards"]:
            cards.remove(card)
            if (card.rank == 14):
                cards.remove(0)
        result2 = two_of_a_kind(cards, [])
        if (result2 != None):
            top_cards = result["top_cards"] + result2["top_cards"]
            return {"hand_ranking": 3,
                    "top_cards": top_cards,
                    "top_hand": top_cards}
    return None
@_log_function
def flush(hand, board):
    cards = get_flush_cards(hand, board)
    if (cards != None):
        #input("returning")
        print(cards[-5:])
        #input("ok?")
        return {"hand_ranking": 4, "top_cards": cards[-5:], "top_hand": cards[-5:]}
    return None

@_log_function
def get_flush_cards(hand, board):
    sorted_cards = sort_cards_by_suit(hand, board)
    cards = None
    if (len(sorted_cards["spades"]) >= 5):
        cards = prep_cards(sorted_cards["spades"], [])
    elif (len(sorted_cards["diamonds"]) >= 5):
        cards = prep_cards(sorted_cards["diamonds"], [])
    elif (len(sorted_cards["hearts"]) >= 5):
        cards = prep_cards(sorted_cards["hearts"], [])
    elif (len(sorted_cards["clubs"]) >= 5):
        cards = prep_cards(sorted_cards["clubs"], [])
    return cards

@_log_function
def straight(hand, board):
    cards = prep_cards(hand, board)
    print(cards)
    #input("in straight - prep result")
    i = len(cards) - 1
    while (i - 4 >= 0):
        if (cards[i].rank - cards[i-1].rank == 1
            and cards[i-1].rank - cards[i-2].rank == 1
            and cards[i-2].rank - cards[i-3].rank == 1
            and cards[i-3].rank - cards[i-4].rank == 1):
            top_cards = [cards[i], cards[i-1],
                            cards[i-2], cards[i-3],
                            cards[i == cards[i-2].suit - 4]]
            return {"hand_ranking": 5,
                    "top_cards": top_cards,
                    "top_hand": top_cards}
        i -= 1
    #input("didn't find straight")
    return None

@_log_function
def three_of_a_kind(hand, board):
    print("starting three of a kind")
    cards = prep_cards(hand, board)
    for card in cards:
        print(card)
    i = len(cards) - 1
    while (i - 2 >= 0):
        if (cards[i].rank == cards[i-1].rank == cards[i-2].rank):
            #input("found pair:{},{}".format(str(cards[i]),str(cards[i-1])))
            top_cards = cards[i-2:i+1]
            top_hand = copy.copy(top_cards)
            for j in range(0, len(cards)):
                #input("ok1...{}".format(j))
                if (len(cards)-1-j > i or len(cards)-1-j < i-2):
                    #input("ok2...j:{} i:{}".format(len(cards)-1-j, i))
                    top_hand.append(cards[j])
                    if (len(top_hand) == 5):
                        print("found three of a kind")
                        return {"hand_ranking": 6,
                                "top_cards": top_cards,
                                "top_hand": top_hand}
        i -= 1
    print("didn't find three of a kind")
    return None

@_log_function
def two_pair(hand, board):
    print("starting two_pair")
    result = two_of_a_kind(hand, board)
    if (result != None):
        print("Top cards:")
        for card in result["top_cards"]:
            print(str(card))
        cards = prep_cards(hand, board)
        for card in result["top_cards"]:
            print("top card: {}".format(str(card)))
            print("Cards:")
            for c in cards:
                print(str(c))
            c = next(c for c in cards if c.rank == card.rank and c.suit == card.suit)
            cards.remove(c)
            if (card.rank == 14):
                del cards[0]
        result2 = two_of_a_kind(cards, [])
        if (result2 != None):
            print("Top cards:")
            for card in result2["top_cards"]:
                print(str(card))
            top_cards = result2["top_cards"]
            for card in result2["top_cards"]:
                print("top card: {}".format(str(card)))
                print("Cards:")
                for c in cards:
                    print(str(c))
                c = next(c for c in cards if c.rank == card.rank and c.suit == card.suit)
                cards.remove(c)
                if (card.rank == 14):
                    del cards[0]
            top_cards += result["top_cards"]
            top_hand = copy.copy(top_cards)
            top_hand.append(cards[-1])
            print("found two pair")
            for card in top_cards:
                print(str(card))
            return {"hand_ranking": 7,
                    "top_cards": top_cards,
                    "top_hand": top_hand}
    print("didn't find two pair")
    return None

def two_of_a_kind(hand, board):
    print("starting two of a kind")
    cards = prep_cards(hand, board)
    for card in cards:
        print(card)
    i = len(cards) - 1
    while (i - 1 >= 0):
        if (cards[i].rank == cards[i-1].rank):
            #input("found pair:{},{}".format(str(cards[i]),str(cards[i-1])))
            top_cards = cards[i-1:i+1]
            top_hand = copy.copy(top_cards)
            for j in range(0, len(cards)):
                #input("ok1...{}".format(j))
                if (len(cards)-1-j > i or len(cards)-1-j < i-1):
                    #input("ok2...j:{} i:{}".format(len(cards)-1-j, i))
                    top_hand.append(cards[j])
                    if (len(top_hand) == 5):
                        print("found two of a kind")
                        return {"hand_ranking": 8,
                                "top_cards": top_cards,
                                "top_hand": top_hand}
        i -= 1
    print("didn't find two of a kind")
    return None

@_log_function
def high_card(hand, board):
    cards = prep_cards(hand, board)
    return {"hand_ranking": 9,
            "top_cards": cards[-1],
            "top_hand": cards[-5:]}

@_log_function
def sort_cards_by_suit(hand, board):
    clubs = []
    spades = []
    hearts = []
    diamonds = []
    cards = copy.copy(hand) + copy.copy(board)
    print(cards)
    cards = sorted(cards,key=lambda card: card.rank)
    for card in cards:
        if (card.suit == 0):
            clubs.append(card)
        elif (card.suit == 1):
            diamonds.append(card)
        elif (card.suit == 2):
            hearts.append(card)
        else:
            spades.append(card)
    return {"clubs":clubs, "spades":spades, "hearts":hearts, "diamonds":diamonds}

@_log_function
def prep_cards(hand, board):
    cards = copy.copy(hand)
    cards = cards + board
    cards = sorted(cards,key=lambda card: card.rank)
    #cards.sort(key=lambda card: card.rank)
    """add aces to end of cards"""
    for card in cards:
        if (card.rank == 1):
            replace = True
            for card2 in cards:
                if (card2.rank == 14 and card.suit == card2.suit):
                    replace = False
            if (replace == True):
                temp_card = copy.copy(card)
                temp_card.rank = 14
                cards.append(temp_card)
        else:
            break
    return cards