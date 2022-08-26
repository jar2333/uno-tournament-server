class Registry:
    def __init__(self):
        self.registered = dict()

    def register_player(self, key):
        self.registered[key] = 0

    def unregister_player(self, key):
        del self.registered[key]

    def is_registered(self, key) -> bool:
        return key in self.registered

    def get_registered(self) -> dict:
        return self.registered

    def record_win(self, key):
        self.registered[key] += 1