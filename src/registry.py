class Registry:
    def __init__(self):
        self.registered = dict()
        self.disqualified = set()

    def register_player(self, key):
        self.registered[key] = 0

    def unregister_player(self, key):
        del self.registered[key]

    def is_registered(self, key) -> bool:
        return key in self.registered

    def disqualify_player(self, key):
        self.disqualified.add(key)

    def is_disqualified(self, key):
        return key in self.disqualified

    def get_registered(self) -> dict:
        return self.registered

    def record_win(self, key):
        if not key is None: #happens in matches with two disqualified players
            self.registered[key] += 1