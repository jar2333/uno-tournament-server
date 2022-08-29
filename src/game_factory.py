import imp
from game import Game

from uno_game import UnoGame

def get_new_game(player1: str, player2: str) -> Game:
    return UnoGame(player1, player2)