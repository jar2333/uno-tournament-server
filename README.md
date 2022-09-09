# Uno Tournament server

A server to host a round-robin tournament of Uno games. The code can easily be extended and minimally modified to play any two-player turn-based game, however. One only needs to subclass the `Game` class, and change the method in `game_factory.py` to return an instance of the desired Game. Modify this interface code however you like!

The current skeleton code and the `UnoGame` implementation offer a JSON API for interacting with the server through WebSocket:

Game agnostic API:

* When tournament has not started: 

    * Sent messages:
        1. `{"type": "register", "key": "<key>"}`
    
        This command registers the client as a player. Closing the WebSocket connection before the torunament starts will unregister the player, requiring that this command be run again upon reconnection. The <key> field must be one of the unique keys found inside `keys.txt`. This is a unique identifier for the player, and used internally as such.
        
        2. tbd...

* After the tournament has started:
    
    * Received messages:
        1. `{"type": "game_start"}`
        
        Received when a game involving this client has started. If this client is player 1, a message indicating that their turn has started will be sent shortly afterwards (see 3. below).
        
        2. `{"type": "game_ended"}`
        
        Received when a game involving this client has ended.
        
        3. `{"type": "turn_started"}`
        
        Received when the turn for the player associated with this client has started. This will be followed by a message indicating that input is being read (see 5. below)
        
        4. `{"type": "turn_ended"}`
        
        Received when the turn for the player associated with this client has ended. If game has ended, it will be followed by a game ended message (2. above). Otherwise, a turn started message (3. above) will be received when it is the player's turn again.
        
        5. `{"type": "reading_move"}`
        
        Received when server is reading the websocket for commands. Note, that the websocket will buffer all newline-separated commands sent at any time, but will not read them until after this message has been sent to the client. This message also indicates that the timer has been started.
        
        6. `{"type": "invalid_move"}`
        
        Received when message sent by client could not be parsed. It can be assumed that no side-effects occurred. An invalid move does not reset the timer. It is recommended to never have to rely on this message, it is provided for debugging purposes. Followed by a state message (8. below).
        
        7. `{"type": "valid_move"}`
        
        Received when message sent by client was successfully parsed, leading to a game action. This resets the timer. Followed by a state message (8. below).
        
        8. `{"type": "state", "state": <state_dict>, "timer": <time>}`
        
        Received after a game start message (see 1. above), and after a valid or invalid move message (6. and 7. above). Contains a dictionary <state_dict> encoding the state of the game, and a float <time> denoting how many seconds are left in the timer. Note, not all posible moves end the player's turn. An explicit turn ended message (see 4. above) will be sent shortly afterwards if the turn was ended. Otherwise, another reading move message (see 5. above) will be sent instead, indicating that another player move is being read.

`UnoGame` specific API:
* Sent messages;
    1. tbd...

* Received messages
    1. tbd...
