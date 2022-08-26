import asyncio
import websockets

import json
from json.decoder import JSONDecodeError

from round_robin import get_schedule
from game import Game

"""
CURRENT GAMES
"""
#player_key : Game
GAMES = dict()

def add_game(game):
    global GAMES
    p1, p2 = game.get_keys() 
    GAMES[p1] = game
    GAMES[p2] = game

def remove_game(game):
    global GAMES
    p1, p2 = game.get_keys() 
    del GAMES[p1]
    del GAMES[p2]

def get_game(key):
    if key in GAMES:
        return GAMES[key]
    return None

"""
PERMISSIBLE KEYS
"""
KEYS = set()

def parse_keys():
    global KEYS
    with open('keys.txt', 'r') as f:
        for line in f.readlines():
            KEYS.add(line.rstrip('\n'))

"""
REGISTERED KEYS
"""
REGISTERED = set()

def register_player(key):
    global REGISTERED
    REGISTERED.add(key)

def unregister_player(key):
    global REGISTERED
    REGISTERED.remove(key)

def is_registered(key):
    return key in REGISTERED

"""
WEBSOCKETS SERVER LOGIC
"""

def is_valid_init_message(msg):
    return 'type' in msg and msg['type'] == 'init' and 'key' in msg

def has_valid_key(msg):
    key = msg['key']
    return key in KEYS and not key in REGISTERED

#handles any subsequent messages (and publishes messages as well)
async def general_handler(key, websocket):
    await asyncio.Future()

#handles the parsing of init message upon connection
#add a refusal after the signup time has expired
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
            register_player(key)

            #sleep until tournament starts

            #handle further messages from this socket
            await general_handler(key, websocket)
        else:
            raise ValueError('Invalid init message')

    except (JSONDecodeError, ValueError) as e:
        await websocket.close(code=1003, reason=str(e))

    except websockets.ConnectionClosedOK:
        if not key is None and is_registered(key):
            unregister_player(key)

#starts websockets server
async def main():
    async with websockets.serve(init_handler, '', 8001):
        await asyncio.Future()  # run forever

"""
MATCHMAKING AND GAME SIMULATION LOGIC
"""
async def play_game(key_pair):
    player1, player2 = key_pair
    game = Game(player1, player2)

    add_game(game)
    await game.play()
    remove_game(game)

async def match_make():
    #sleep until tournament start
    await asyncio.sleep(5)

    #make round robin schedule
    schedule = get_schedule(REGISTERED)

    #iterate through round robin rounds
    for round in schedule:
        coroutines = [play_game(pair) for pair in round]

        #games played in parallel in each round
        game_loop = asyncio.get_event_loop()
        game_loop.run_until_complete(asyncio.gather(*coroutines))
        game_loop.close()

    print("All games played. Ending...")

"""
MAIN SCRIPT
"""
if __name__ == '__main__':
    #parse keys
    parse_keys()
    print(KEYS)

    #run websockets server
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        main(),
        match_make()
    ))
    loop.close()