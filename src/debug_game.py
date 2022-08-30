from game import Game
from messages import is_valid_message

class DebugGame(Game):
    def __init__(self, p1: str, p2: str):
        super().__init__(p1, p2)

    def interpret_message(self, key: str, message: dict) -> bool:
        return is_valid_message(message)

    def get_state(self) -> dict:
        return {"turn": self.player1_key}