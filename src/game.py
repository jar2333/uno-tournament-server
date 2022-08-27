import asyncio

class Game:
    def __init__(self, player1: str, player2: str):
        self.player1_key  = player1
        self.player2_key  = player2
        self.player1_hand = []
        self.player2_hand = []
        self.discard_pile = []
        self.draw_pile    = []

        self.winner = None

        #Event objects
        self.is_turn_events = {player1: asyncio.Event(), player2: asyncio.Event()}
        self.is_finished_event = asyncio.Event()

    def get_start_state(self) -> dict:
        return {} #response

    def play(self, message) -> dict:
        return {} #response

    def is_finished(self) -> bool:
        return self.is_finished_event.is_set()

    def get_winner(self) -> str:
        return self.winner

    def set_winner(self, winner_key):
        self.winner = winner_key
        self.is_finished_event.set()

    def subscribe_is_turn(self, player_key) -> asyncio.Event:
        return self.is_turn_events[player_key]

    def subscribe_is_finished(self) -> asyncio.Event:
        return self.is_finished_event