from game import Game

from random import shuffle

COLORS = ["red", "blue", "yellow", "green"]

ONE_MORE = ["skip", "reverse", "+2", "+4"]

class UnoGame(Game):
    def __init__(self, p1: str, p2: str):
        super().__init__(p1, p2)

        #make deck, fill and shuffle draw pile
        self.draw_pile = make_deck()
        shuffle(self.draw_pile)

        #initialize hands
        self.hands = {self.player1_key: [], self.player2_key: []}
        
        #draw initial cards to hands
        for key in self.hands:
            for i in range(7):
                card = self.draw_pile.pop()
                self.hands[key].append(card)

        #initialize discard pile
        self.discard_pile = []
        while True:
            card = self.draw_pile.pop()
            number, color = card
            if number in ["wild", "+4"]:
                self.draw_pile = [card] + self.draw_pile
            else:
                self.discard_pile.append(card)
                break

        #a bunch of flags used for implementing game rules
        self.has_drawn = False

        #for +4 challenges
        self.hand_revealed = False

        #if color is requested
        self.color_requested = False

        #if challenge is offered
        self.challenge_offered = False

        #if uno was called

    def interpret_message(self, key: str, message: dict):
        hand = self.hands[key]
        opponent_key = self.get_opponent_key(key)
        match message:
            case {'type': 'draw'}:
                if self.color_requested or self.challenge_offered or self.has_drawn: #drawn card must be played
                    return None

                card = self.__draw_card(key)

                #if drawn card can be played, it must
                if self.__is_valid(card):
                    #hence, turn doesn't end, and we must note the drawn card
                    self.has_drawn = True
                    return False

                #otherwise, turn ends
                return True

            case {'type': 'play', 'index': index}:
                if self.color_requested or self.challenge_offered:
                    return None
                try:
                    i = int(index)

                    #must play drawn card if a card was drawn this turn
                    if self.has_drawn and i != len(hand)-1:
                        return None

                    card = hand[i]

                    if not self.__is_valid(card):
                        return None

                    number, color = card

                    if color == "colorless":
                        self.color_requested = True
                        return False
                    else:
                        self.discard_pile.append(card)

                    self.hands[key].pop(i)

                    if number in ["skip", "reverse", "+2"]:
                        match number:
                            case "+2":
                                for i in range(2):
                                    self.__draw_card(opponent_key)
                            case _:
                                pass

                        return False

                    #End of turn, reset flag
                    self.has_drawn = False
                    return True

                except:
                    return None

            case {'type': 'play', 'index': index, 'color': chosen_color}:
                if self.color_requested or self.challenge_offered: #must be in standalone 'color' message
                    return None
                try:
                    i = int(index)

                    #must play drawn card if a card was drawn this turn
                    if self.has_drawn and i != len(hand)-1:
                        return None

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
                                #+4 played, so challenge offered. This ends the turn as well, to allow for challenge.
                                self.challenge_offered = True
                                self.has_drawn = False
                                return True
                            case _:
                                pass

                        return False

                    #End of turn, reset flag
                    self.has_drawn = False
                    return True

                except:
                    return None

            case {'type': 'challenge', 'challenge': did_challenge}:
                if not self.challenge_offered:
                    return None

                self.challenge_offered = False

                if did_challenge: #hand is revealed
                    self.hand_revealed = True
                    for card in self.hands[opponent_key]:
                        if self.__is_valid(card) and card != ("+4", "colorless"): 
                            #if there was a non +4 card that couldve been played
                            #challenge won, opponent draws 4, turn continues
                            for i in range(4):
                                self.__draw_card(opponent_key)
                            return False
                    #challenge lost, player draws 6, turn ends
                    for i in range(6):
                        self.__draw_card(key)
                    self.has_drawn = False
                    return True

                else:
                    #draw 4 and end turn
                    for i in range(4):
                        self.__draw_card(key)
                        
                    self.has_drawn = False
                    return True

            case {'type': 'color', 'color': chosen_color}:
                if self.challenge_offered or (not self.color_requested) or (not chosen_color in COLORS):
                    return None
                
                number, _ = self.discard_pile[-1]
                self.discard_pile[-1] = (number, chosen_color)
                self.color_requested = False

                #if the card was a +4, challenge is available to opponent.
                if number == "+4":
                    self.challenge_offered = True

                self.has_drawn = False
                return True #turn ends, because this only happens if wild/+4 card played :)

            # case {'type': 'uno'}:
            #     pass

            case _:
                return None

    def get_state(self, key: str):
        if len(self.discard_pile) == 0:
            d = None
        else:
            d = self.discard_pile[-1]

        opponent_key = self.get_opponent_key(key)
        opponent_hand_size = len(self.hands[opponent_key])

        #Prompt fields says if a specific action is requested
        state = {"player_hand": self.hands[key], "discard": d, "opponent_hand_size": opponent_hand_size, "prompt": None}
        if self.color_requested:
            state['prompt'] = 'color'
        elif self.challenge_offered:
            state['prompt'] = 'challenge'

        if self.hand_revealed:
            state['opponent_hand'] = self.hands[opponent_key]
            self.hand_revealed = False

        return state

    def __is_valid(self, card):
        number, color = card
        
        discard_number, discard_color = self.discard_pile[-1]

        if number == discard_number or color == discard_color or number == "wild":
            return True

        return False

    def __draw_card(key):
        #draw 1 from draw_pile and reshuffle discard if necessary
        #make sure to reset all wild and +4 to colorless
        #return drawn
        return ("", "")


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
            
