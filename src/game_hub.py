from game import Game
import asyncio


#USAGE OF ASYNCIO EVENTS:
#have events for when game created, and when game finished!
class GameHub:
    def __init__(self):
        self.games    = dict()

        self.created  = dict()
    
    #This calls set() on the corresponding game_created events
    def add_game(self, p1, p2) -> Game:
        for key in (p1, p2):
            if not key in self.created:
                self.created[key] = asyncio.Event()
            self.created[key].set()

        game = Game(p1, p2)
        self.games[p1] = game
        self.games[p2] = game

        return game

    def remove_game(self, p1, p2):
        #once game removed, block until new is created
        for key in (p1, p2):
            if not key in self.created:
                self.created[key] = asyncio.Event()
            self.created[key].clear()

        del self.games[p1]
        del self.games[p2]

    def get_game(self, key) -> Game:
        if key in self.games:
            return self.games[key]
        return None

    def subscribe_game_created(self, key) -> asyncio.Event:
        #lazy initialization
        if not key in self.created:
            self.created[key] = asyncio.Event()
        return self.created[key]