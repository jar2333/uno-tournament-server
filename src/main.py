import asyncio
import websockets

import json
from json.decoder import JSONDecodeError

class Game:
    def __init__(self, player1, player2):
        pass

    async def play(self):
        pass

"""
WEBSOCKETS SERVER LOGIC
"""
KEYS = set()

REGISTERED = dict() #player_key : websocket

def is_valid_init_message(msg):
    return 'type' in msg and msg['type'] == 'init' and 'key' in msg

def has_valid_key(msg):
    key = msg['key']
    return key in KEYS and not key in REGISTERED

def register_player(websocket, key):
    global REGISTERED
    REGISTERED[key] = websocket

def unregister_player(key):
    global REGISTERED
    del REGISTERED[key]

def is_registered(key):
    return key in REGISTERED

#handles any subsequent messages (and publishes messages as well)
async def general_handler(key, websocket):
    await asyncio.Future()

#handles the parsing of init message upon connection
async def init_handler(websocket):
    key = None
    try:
        #receive message from client
        msg = json.loads(await websocket.recv())
        print(f"msg received: {msg}")

        if is_valid_init_message(msg) and has_valid_key(msg):
            key = msg['key']

            #register player
            print(f"registered player {key}")
            register_player(websocket, key)

            #handle further messages from this socket
            await general_handler(key, websocket)
        else:
            raise ValueError('Not valid init message')

    except (JSONDecodeError, ValueError) as e:
        await websocket.close(code=1003, reason=str(e))

    except websockets.ConnectionClosedOK:
        if not (key is None) and is_registered(key):
            unregister_player(key)

#starts websockets server
async def main():
    async with websockets.serve(init_handler, '', 8001):
        await asyncio.Future()  # run forever

"""
MATCHMAKING AND GAME SIMULATION LOGIC
"""
async def match_make():
    await asyncio.Future()

if __name__ == '__main__':
    #parse keys
    with open('keys.txt', 'r') as f:
        for line in f.readlines():
            KEYS.add(line.rstrip('\n'))
    print(KEYS)

    #run websockets server
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        main(),
        match_make()
    ))
    loop.close()