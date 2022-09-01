from game import Game

from random import shuffle

class UnoGame(Game):
    def __init__(self, p1: str, p2: str):
        super().__init__(p1, p2)

        self.draw_pile = make_deck()
        shuffle(self.draw_pile)

        self.player1_hand = []
        self.player2_hand = []
        
        for i in range(7):
            card = self.draw_pile.pop()
            self.player1_hand.append(card)

        for i in range(7):
            card = self.draw_pile.pop()
            self.player2_hand.append(card)

        self.discard_pile = []

    def interpret_message(self, key: str, message: dict):
        pass

    def get_state(self):
        return {}

def make_deck():
    cards = []
    for number in [str(x) for x in range(10)] + ["skip", "reverse", "+2", "wild", "+4"]:
        if number in ["wild", "+4"]:
            cards.append((number, None))
        else:
            for color in ["red", "blue", "yellow", "green"]:
                amount = 2
                if number == "0":
                    amount = 1
                for i in range(amount):
                    cards.append((number, color))
    
    return cards

def parse(msg):
    match msg:
        case {'type': 'draw'}:
            pass

        case {'type': 'play', 'index': i}:
            pass

        case {'type': 'challenge'}:
            pass

        case {'type': 'uno'}:
            pass

        case _:
            pass

    return (None, False)
            
