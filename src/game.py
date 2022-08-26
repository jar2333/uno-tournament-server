import asyncio

class Game:
    def __init__(self, player1, player2):
        self.player1_key  = player1
        self.player2_key  = player2
        self.player1_hand = []
        self.player2_hand = []
        self.discard_pile = []
        self.draw_pile    = []

    def play(self, message):
        return {} #response

    def get_keys(self):
        return (self.player1_key, self.player2_key)