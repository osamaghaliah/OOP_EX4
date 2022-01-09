class Vertex:
    def __init__(self, key: int, pos: tuple = None):
        self.Key = key
        self.EdgesGoingOutside = dict()
        self.EdgesGoingInside = dict()
        self.pos = pos

    def __repr__(self):
        return "{}: |edges out| {} |edges in| {}".format(self.Key, len(self.EdgesGoingOutside),
                                                         len(self.EdgesGoingInside))

    def getKey(self):
        return self.Key
