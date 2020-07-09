class UnknownType:
    def __init__(self):
        pass

    def from_json(self, json, classname):
        raise NotImplementedError()

    def __repr__(self):
        return "<Unknown Class>"
