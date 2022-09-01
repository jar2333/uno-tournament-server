from venv import create
from registry import Registry

"""
CONTAINS GAME AGNOSTIC MESSAGE API COMPONENTS
"""

#main.py constants and functions
REGISTERED_MESSAGE   = {"type": "registered"}
START_GAME_MESSAGE   = {"type": "game_start"}
ENDED_GAME_MESSAGE   = {"type": "game_ended"}
START_TURN_MESSAGE   = {"type": "turn_start"}
ENDED_TURN_MESSAGE   = {"type": "turn_ended"}
VALID_MOVE_MESSAGE   = {"type": "valid_move"}
INVALID_MOVE_MESSAGE = {"type": "invalid_move"}


WIN_MESSAGE  = {"type": "win"}
LOSE_MESSAGE = {"type": "lose"}

def is_valid_init_message(msg):
    return 'type' in msg and msg['type'] == 'register' and 'key' in msg

def has_valid_key(msg, keys, registry: Registry):
    key = msg['key']
    return key in keys and not registry.is_registered(key)

def create_state_message(state_information: dict):
    return {"type": "state", "state": state_information}
