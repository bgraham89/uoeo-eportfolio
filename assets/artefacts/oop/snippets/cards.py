'''Example classes for card related objects for illustrating elementary OOP concepts'''

from functools import reduce
from random import randint

class Card(object):
    '''Class representing a card.'''
    def __init__(self, suit, value):
        self._SUITS = (
            "♠","♡","♢","♣"
        )
        self._VALUES = (
            "2","3","4","5","6","7","8",
            "9","10","J","Q","K","A"
        )
        self.suit = self._SUITS[suit]
        self.value = self._VALUES[value]

class Deck(list):
    '''Class representing a deck.'''
    def __init__(self):
        super.__init__(self)  
        self.extend([Card(s, v) for s in range(4) for v in range(13)])


class IntegerCard(Card):
    '''Class extending the Card class.'''
    def __init__(self, suit, value):
        super.__init__(self, suit, value)  
        self._PRIMES = (
            2, 3, 5, 7, 11, 13, 17,
            19, 23, 29, 31, 37, 41
        )
        self._integer = (
            self._PRIMES[value]
            + (value << 8)
            + ((2 ** suit) << 12)
            + ((2 ** value) << 16)
        )
    
    def __int__(self):
        return self._integer
    

class PokerHand(list):
    '''Class representing a poker hand.'''
    def __init__(self, amount_cards):
        super.__init__(self, amount_cards)  
        self._CreateCards(amount_cards)
    
    def _CreateCards(self, amount_cards=5):
        while True:
            cards = [IntegerCard(randint(0,3), randint(0,12)) for _ in range(amount_cards)]
            if len(set(cards)) == amount_cards:
                self.extend(cards)
                break
    
    def HasFlush(self):
        return reduce(lambda x, y: int(x) & int(y), self) & (15 << 12) > 0
    
    def HasPair(self):
        return bin(reduce(lambda x, y: int(x) & int(y), self) & (4096 << 16)).count("1") < len(self)

