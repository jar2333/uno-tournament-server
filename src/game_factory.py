import imp
from game import Game

from uno_game import UnoGame
from debug_game import DebugGame

def get_new_game(player1: str, player2: str) -> Game:
    return DebugGame(player1, player2)