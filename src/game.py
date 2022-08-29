import asyncio
from abc import ABC, abstractmethod

class Game(ABC):
    def __init__(self, player1: str, player2: str):
        self.player1_key  = player1
        self.player2_key  = player2

        self.winner = None

        #Event objects
        self.is_turn_events = {player1: asyncio.Event(), player2: asyncio.Event()}
        self.is_finished_event = asyncio.Event()


    @abstractmethod
    def __interpret_message(self, key: str, message: dict) -> dict:
        return {}

    @abstractmethod
    def get_start_state(self) -> dict:
        return {}

    def play(self, key, message) -> dict:
        response = self.__interpret_message(key, message)

        #set the turn start/end events
        self.is_turn_events[key].clear()
        self.is_turn_events[self.__get_opponent_key(key)].set()
        return response

    def is_finished(self) -> bool:
        return self.is_finished_event.is_set()

    def get_winner(self) -> str:
        return self.winner

    def forfeit(self, key):
        self.set_winner(self.__get_opponent_key(key))

    def subscribe_is_turn(self, player_key) -> asyncio.Event:
        return self.is_turn_events[player_key]

    def subscribe_is_finished(self) -> asyncio.Event:
        return self.is_finished_event

    def set_winner(self, winner_key):
        self.winner = winner_key #set winner first, then set as finished
        self.is_finished_event.set()

    def __get_opponent_key(self, key):
        if key == self.player1_key:
            return self.player2_key
        else:
            return self.player1_key