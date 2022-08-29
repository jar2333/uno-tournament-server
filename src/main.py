import asyncio
import imp
import websockets

import json
from json.decoder import JSONDecodeError

from round_robin import get_schedule
from registry import Registry
from game_hub import GameHub

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
REGISTRY = Registry()

"""
CURRENT GAMES
"""
GAMES = GameHub()

TOURNAMENT_IS_OVER = False

TURN_TIMEOUT_IN_SECONDS = 15.0

"""
WEBSOCKETS SERVER LOGIC
"""
def is_valid_init_message(msg):
    return 'type' in msg and msg['type'] == 'init' and 'key' in msg

def has_valid_key(msg):
    key = msg['key']
    return key in KEYS and not REGISTRY.is_registered(key)

#handles any subsequent messages (and publishes messages as well)
async def general_handler(key, websocket):
    while not TOURNAMENT_IS_OVER:
        #wait until new game for key is created
        game_created_event = GAMES.subscribe_game_created(key)
        await game_created_event.wait()

        #Get game and send the current (init) state to the client.
        #This is the indication that they can start sending messages.
        game = GAMES.get_game(key)
        if game is None: #shouldn't happen, but just in case it does...
            continue
        websocket.send(json.dumps(game.get_start_state()))

        while not game.is_finished():

            #wait until it is this player's turn to start reading.
            #this has the added bonus that if the client message was not processed
            #successfully, this will still be set() (nonblocking), so it will try again
            is_turn_event = game.subscribe_is_turn(key)
            await is_turn_event.wait()

            #game start timer?
            try:
                """
                ADD TIMING!!!
                """
                text = asyncio.wait_for(websocket.recv(), timeout=TURN_TIMEOUT_IN_SECONDS)
                message = json.loads(text)

                #Game can either end turn here or finish entirely.
                #In case of invalid action, nothing occurs (null response).
                #figure out turn timeout in context of null response (needs more sophisticated timing)
                response = game.play(key, message) 

                #send response to client
                await websocket.send(json.dumps(response))
            except asyncio.TimeoutError:
                #make the player lose (set winner && finish game)!
                game.forfeit(key)
            except JSONDecodeError:
                pass

        #Past while loop, game is finished
        #wait for game to be removed from GameHub 
        game_removed_event = GAMES.subscribe_game_removed(key)
        await game_removed_event.wait()


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
            REGISTRY.register_player(key)

            #sleep until tournament starts

            #handle further messages from this socket
            await general_handler(key, websocket)
        else:
            raise ValueError('Invalid init message')

    except (JSONDecodeError, ValueError) as e:
        await websocket.close(code=1003, reason=str(e))

    except websockets.ConnectionClosed:
        if not key is None and REGISTRY.is_registered(key):
            REGISTRY.unregister_player(key)

#starts websockets server
async def main():
    async with websockets.serve(init_handler, '', 8001):
        await asyncio.Future()  # run forever

"""
MATCHMAKING AND GAME SIMULATION LOGIC
"""
async def play_game(key_pair):
    player1, player2 = key_pair

    #win by default checks (happens when # of players is uneven)
    if player1 is None:
        return player2
    elif player2 is None:
        return player1

    #add game to hub
    game = GAMES.add_game(player1, player2)

    #wait until game is finished!
    game_ended_event = game.subscribe_is_finished()
    await game_ended_event.wait()

    #Get winner of game
    winner = game.get_winner() 

    #remove game from hub
    GAMES.remove_game(player1, player2)

    return winner

async def match_make():
    global TOURNAMENT_IS_OVER
    #sleep until tournament start

    #make round robin schedule
    schedule = get_schedule(REGISTRY.get_registered())

    #iterate through round robin rounds
    for round in schedule:
        coroutines = [play_game(pair) for pair in round]

        #Games played in parallel in each round
        #results contains the winning keys of each game

        game_loop = asyncio.get_event_loop()
        results = game_loop.run_until_complete(asyncio.gather(*coroutines))
        game_loop.close()

        #tally up the score for winning players
        for key in results:
            REGISTRY.record_win(key)

    print("All games played. Ending...")
    TOURNAMENT_IS_OVER = True #makes all coroutines spawned by websocket server end

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