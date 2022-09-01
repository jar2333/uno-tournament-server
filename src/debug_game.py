from game import Game

class DebugGame(Game):
    def __init__(self, p1: str, p2: str):
        super().__init__(p1, p2)

    def interpret_message(self, key: str, message: dict):
        if 'type' in message and message['type'] == 'debug':
            return True
            
        return None

    def get_state(self, key: str) -> dict:
        return {"turn": self.player1_key}
