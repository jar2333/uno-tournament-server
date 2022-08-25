import asyncio
import websockets

import json
from json.decoder import JSONDecodeError

KEYS = set()

#key : websocket
QUEUED = dict()

#(player1_key, player2_key) : Game (object)
GAMES = dict()


def is_valid_init_message(msg):
    return msg is dict and 'type' in msg and msg['type'] == 'init' and 'key' in msg


def queue_player(websocket, key):
    global QUEUED
    QUEUED[key] = websocket


def unqueue_player(key):
    global QUEUED
    del QUEUED[key]


async def init_handler(websocket):
    key = None
    try:
        msg = json.loads(await websocket.recv())
        if is_valid_init_message(msg):
            key = msg['key']
            if key in KEYS and not key in QUEUED:
                queue_player(websocket, key)
            else:
                websocket.close(reason='INVALID KEY IN INIT MESSAGE!')
    except JSONDecodeError:
        websocket.close(reason='INVALID MESSAGE!')
    except websockets.ConnectionClosedOK:
        if not (key is None) and key in QUEUED:
            unqueue_player(key)


async def main():
    async with websockets.serve(init_handler, '', 8001):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    #parse keys
    with open('keys.txt', 'r') as f:
        for line in f.readlines():
            KEYS.add(line.rstrip('\n'))

    #run websockets server
    asyncio.run(main())

    print("launched server")