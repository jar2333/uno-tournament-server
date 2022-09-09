# Uno Tournament server

A server to host a round-robin tournament of Uno games. The code can easily be extended and minimally modified to play any two-player turn-based game, however. One only needs to subclass the `Game` class, and change the method in `game_factory.py` to return an instance of the desired Game. Modify this interface code however you like!

The current skeleton code and the `UnoGame` implementation offer a JSON API for interacting with the server through WebSocket:

Game agnostic API:
- tbd

`UnoGame` specific API:
- tbd
