class Registry:
    def __init__(self):
        self.registered = set()

    def register_player(self, key):
        self.registered.add(key)

    def unregister_player(self, key):
        self.registered.remove(key)

    def is_registered(self, key):
        return key in self.registered

    def get_registered(self):
        return self.registered