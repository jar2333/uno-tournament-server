from game import Game
from messages import is_valid_message

class DebugGame(Game):
    def __init__(self, p1: str, p2: str):
        super().__init__(p1, p2)

    def interpret_message(self, key: str, message: dict) -> dict:
        if not is_valid_message(message):
            return None

        return {"type": "state", "turn": key, "echo": str(message)}

    def get_state(self) -> dict:
        return {"type": "state", "turn": self.player1_key}