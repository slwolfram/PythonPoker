class Hand_result(object):

    """rank: integer 0-8"""
    """0: none"""
    """1: straight flush"""
    """2: four of a kind"""
    """3: full house"""
    """4: flush"""
    """5: straight"""
    """6: three of a kind"""
    """7: two of a kind"""
    """8: high card"""

    def __init__(self):
        self.rank = 0
        self.best_hand = []
