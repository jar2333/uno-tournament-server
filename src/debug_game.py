from game import Game

def is_valid_debug_message(message: dict) -> bool:
    if not 'type' in message:
        return False

    #debug
    if message['type'] != 'debug':
        return False

    return True

class DebugGame(Game):
    def __init__(self, p1: str, p2: str):
        super().__init__(p1, p2)

    def interpret_message(self, key: str, message: dict) -> bool:
        return is_valid_debug_message(message)

    def get_state(self) -> dict:
        return {"turn": self.player1_key}