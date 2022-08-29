from game import Game
import asyncio


#USAGE OF ASYNCIO EVENTS:
#have events for when game created, and when game finished!
class GameHub:
    def __init__(self):
        self.games    = dict()

        self.created  = dict()
        self.removed  = dict()
    
    #This calls set() on the corresponding game_created events
    def add_game(self, p1, p2) -> Game:

        #create game
        game = Game(p1, p2)
        self.games[p1] = game
        self.games[p2] = game

        #signal its availability
        for key in (p1, p2):
            if not key in self.created:
                self.created[key] = asyncio.Event()
            self.created[key].set()

        return game

    def remove_game(self, p1, p2):
        #mark game as no longer available
        for key in (p1, p2):
            self.created[key].clear()

        #remove game
        del self.games[p1]
        del self.games[p2]

        #send game_removed event (Game will be removed)
        for key in (p1, p2):
            self.removed[key].set()

        #reset game_removed flag 
        #(game_removed_event.wait() in other coroutine will have passed, 
        # coroutine then blocked at await game_created_event.wait())
        for key in (p1, p2):
            self.removed[key].clear()

    def get_game(self, key) -> Game:
        if key in self.games:
            return self.games[key]
        return None

    def subscribe_game_created(self, key) -> asyncio.Event:
        #lazy initialization of both created and removed
        if not key in self.created:
            self.created[key] = asyncio.Event()
            self.removed[key] = asyncio.Event()

        return self.created[key]

    def subscribe_game_removed(self, key) -> asyncio.Event:
        return self.removed[key]