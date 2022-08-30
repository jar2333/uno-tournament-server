from game import Game

class UnoGame(Game):
    def __init__(self, p1: str, p2: str):
        super().__init__(p1, p2)

        self.draw_pile =    []
        self.discard_pile = []
        self.player1_hand = []
        self.player2_hand = []

    def interpret_message(self, key: str, message: dict) -> dict:
        return {}

    def get_state(self) -> dict:
        return {}