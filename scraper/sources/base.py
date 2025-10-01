class BaseSource:
    name = "base"
    def search(self, states, query, limit=100):
        raise NotImplementedError
