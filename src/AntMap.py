

NORTH = 1
EAST  = 2
SOUTH = 3
WEST  = 4

class AntMap:
    def __init__(self, map_definition=None):
        self.ant_location = (0,0, EAST)
        self.start_location = (0,0)
        self.end_location   = (0,0)
        self.map = ()

        if map_definition:
            self._load_definition(map_definition)


    def _load_definition(map_definition):
        pass
