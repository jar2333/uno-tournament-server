from game import Game

class GameHub:
    def __init__(self):
        self.games = dict()
    
    def add_game(self, p1, p2):
        # p1, p2 = game.get_keys() 
        game = Game(p1, p2)
        self.games[p1] = game
        self.games[p2] = game
        return game

    def remove_game(self, p1, p2):
        del self.games[p1]
        del self.games[p2]

    def get_game(self, key):
        if key in self.games:
            return self.games[key]
        return None