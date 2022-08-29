from registry import Registry

START_TURN_MESSAGE = {"type": "start_turn"}

def is_valid_message(message: dict) -> bool:
    if not 'type' in message:
        return False

    #debug
    if message['type'] != 'debug':
        return False

    return True

def is_valid_init_message(msg):
    return 'type' in msg and msg['type'] == 'init' and 'key' in msg

def has_valid_key(msg, keys, registry: Registry):
    key = msg['key']
    return key in keys and not registry.is_registered(key)
