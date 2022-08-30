from registry import Registry

#main.py messages
REGISTERED_MESSAGE   = {"type": "registered"}
START_GAME_MESSAGE   = {"type": "game_start"}
ENDED_GAME_MESSAGE   = {"type": "game_ended"} #add winner field?
START_TURN_MESSAGE   = {"type": "turn_start"}
ENDED_TURN_MESSAGE   = {"type": "turn_ended"} #add state field?
INVALID_MOVE_MESSAGE = {"type": "invalid_move"}

#game.py messages
WIN_MESSAGE  = {"type": "win"}
LOSE_MESSAGE = {"type": "lose"}

def is_valid_message(message: dict) -> bool:
    if not 'type' in message:
        return False

    #debug
    if message['type'] != 'debug':
        return False

    return True

def is_valid_init_message(msg):
    return 'type' in msg and msg['type'] == 'register' and 'key' in msg

def has_valid_key(msg, keys, registry: Registry):
    key = msg['key']
    return key in keys and not registry.is_registered(key)
