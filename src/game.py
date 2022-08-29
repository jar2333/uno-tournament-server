import asyncio
from abc import ABC, abstractmethod

class Game(): #(ABC):
    def __init__(self, player1: str, player2: str):
        self.player1_key  = player1
        self.player2_key  = player2

        self.winner = None

        #Event objects
        self.is_turn_events = {player1: asyncio.Event(), player2: asyncio.Event()}
        self.is_finished_event = asyncio.Event()

        #set player1's is_turn flag
        self.is_turn_events[player1].set()


    @abstractmethod
    def interpret_message(self, key: str, message: dict) -> dict:
        return {}

    @abstractmethod
    def get_start_state(self) -> dict:
        return {}

    async def play(self, key, message) -> dict:
        response = self.interpret_message(key, message)

        #set the turn start/end events
        self.is_turn_events[key].clear()
        self.is_turn_events[self.__get_opponent_key(key)].set()

        #can remove...
        await asyncio.sleep(0.1)
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
        for k in self.is_turn_events:
            self.is_turn_events[k].set() #no longer block for both players

    def __get_opponent_key(self, key):
        if key == self.player1_key:
            return self.player2_key
        else:
            return self.player1_key