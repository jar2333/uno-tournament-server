def is_valid_message(message: dict) -> bool:
    if not 'type' in message:
        return False

    #debug
    if message['type'] != 'debug':
        return False
        
    return True