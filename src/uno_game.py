from game import Game

from random import shuffle

COLORS = ["red", "blue", "yellow", "green"]

ONE_MORE = ["skip", "reverse", "+2", "+4"]

class UnoGame(Game):
    def __init__(self, p1: str, p2: str):
        super().__init__(p1, p2)

        self.draw_pile = make_deck()
        shuffle(self.draw_pile)

        self.hands = {self.player1_key: [], self.player2_key: []}
        
        for key in self.hands:
            for i in range(7):
                card = self.draw_pile.pop()
                self.hands[key].append(card)

        self.discard_pile = []

        #a bunch of flags used for implementing game rules

    def interpret_message(self, key: str, message: dict):
        hand = self.hands[key]
        opponent_key = self.get_opponent_key(key)
        match message:
            case {'type': 'draw'}:
                pass

            case {'type': 'play', 'index': index}:
                pass

            case {'type': 'play', 'index': index, "color": chosen_color}:
                try:
                    i = int(index)
                    card = hand[i]

                    if not self.__is_valid(card):
                        return None

                    number, color = card

                    if color == "colorless":
                        if chosen_color in COLORS:
                            self.discard_pile.append((number, chosen_color))
                        else:
                            return None
                    else:
                        self.discard_pile.append(card)

                    self.hands[key].pop(i)

                    if number in ["skip", "reverse", "+2", "+4"]:
                        match number:
                            case "+2":
                                for i in range(2):
                                    self.__draw_card(opponent_key)
                            case "+4":
                                for i in range(4):
                                    self.__draw_card(opponent_key)
                            case _:
                                pass
                            
                        return False

                    return True

                except:
                    return None

            case {'type': 'challenge'}:
                pass

            case {'type': 'uno'}:
                pass

            case _:
                return None

    def get_state(self, key: str):
        if len(self.discard_pile) == 0:
            d = None
        else:
            d = self.discard_pile[-1]

        opponent_key = self.get_opponent_key(key)
        opponent_hand_size = len(self.hands[opponent_key])

        return {"player_hand": self.hands[key], "discard": d, "opponent_hand_size": opponent_hand_size}

    def __is_valid(self, card):
        number, color = card
        
        discard_number, discard_color = self.discard_pile[-1]

        if number == discard_number or color == discard_color or number == "wild":
            return True

        return False

    # def __evaluate_action(self, key, card):
    #     #evaluate effect of action cards
    #     pass

    def __draw_card(key):
        #draw 1 from draw_pile and cycle discard if necessary
        pass


def make_deck():
    cards = []
    for number in [str(x) for x in range(10)] + ["skip", "reverse", "+2", "wild", "+4"]:
        if number in ["wild", "+4"]:
            for i in range(4):
                cards.append((number, "colorless"))
        else:
            for color in COLORS:
                amount = 2
                if number == "0":
                    amount = 1
                for i in range(amount):
                    cards.append((number, color))
    
    return cards
            
