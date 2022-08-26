from game import Game
import asyncio


#USAGE OF ASYNCIO EVENTS:
#have events for when game created, and when game finished!
class GameHub:
    def __init__(self):
        self.games = dict()
    
    #This calls set() on the corresponding game_created events
    def add_game(self, p1, p2):
        game = Game(p1, p2)
        self.games[p1] = game
        self.games[p2] = game

    def remove_game(self, p1, p2):
        del self.games[p1]
        del self.games[p2]

    def get_game(self, key) -> Game:
        if key in self.games:
            return self.games[key]
        return None

    #note: the game_ended event will only be set() once 
    #   BOTH player keys have called this method.
    #   this ensures that no communication to the game 
    #   is being conducted, hence it can be removed from hub.    
    def set_game_ended_for(self, key):
        pass

    def register_game_created(self, key) -> asyncio.Event:
        return asyncio.Event() #asyncio.Event to be awaited. Store in a dict

    def register_game_ended(self, p1_key, p2_key) -> asyncio.Event:
        return asyncio.Event() #asyncio.Event to be awaited.Store in a dict