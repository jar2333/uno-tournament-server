import asyncio

class Game:
    def __init__(self, player1, player2):
        self.player1_key  = player1
        self.player2_key  = player2
        self.player1_hand = []
        self.player2_hand = []
        self.discard_pile = []
        self.draw_pile    = []

        self.winner = None

        #event objects to .wait(), set() when corresponding turn starts, clear() when ends
        self.is_turn = {player1: asyncio.Event(), player2: asyncio.Event()}

    def get_start_state(self) -> dict:
        return {} #response

    def play(self, message) -> dict:
        return {} #response

    def is_finished(self) -> bool:
        return False

    def get_winner(self) -> str:
        return self.winner

    def register_is_turn(self, player_key) -> asyncio.Event:
        return self.is_turn[player_key]