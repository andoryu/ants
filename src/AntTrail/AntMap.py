import json
from pprint import pprint
import sys


NORTH = 1
EAST  = 2
SOUTH = 3
WEST  = 4

BOUNDED = 1
UNBOUNDED = 2

class AntMap:
    def __init__(self, map_definition_file=""):
        self.ant_location = (0,0, EAST)
        self.ant_facing = EAST
        self.end_location   = [0,0]
        self.map = []
        self.size = (0,0)
        self.style = BOUNDED
        self.name = "unnamed"
        self.start_location = [0,0]
        self.trail = []
        self.trail_pos = 0
        self.trail_len = 0

        self.loaded = False

        if map_definition_file:
            self.loaded = self.load_definition(map_definition_file)

    def ant_advance(self):
        facing  = self.ant_location[2]

        if facing == NORTH:
            shift = (  0, -1 )
        if facing == EAST:
            shift = (  1,  0 )
        if facing == SOUTH:
            shift = (  0,  1 )
        if facing == WEST:
            shift = ( -1,  0 )

        new_x = self.ant_location[0] + shift[0]
        new_y = self.ant_location[1] + shift[1]

        #bounds check
        if new_x < 0:
            new_x = 0
        elif new_x >= self.size[0]:
            new_x = self.size[0]-1

        if new_y < 0:
            new_y = 0
        elif new_y >= self.size[1]:
            new_y = self.size[1]-1

        self.ant_location = (new_x, new_y, facing)


        if self.trail_pos < self.trail_len-1:
            if self.trail[self.trail_pos + 1] == [new_x, new_y]:
                self.trail_pos = self.trail_pos + 1

        #return location and view info
        return self._ant_result()


    def _ant_result(self):
        return {
            "loc":  self.ant_location,
            "pos":  self.trail_pos,
            "view": self.get_ant_view(),
            "finished" : [self.ant_location[0], self.ant_location[1]] == self.end_location
        }


    def ant_rotate_ccw(self):
        facing  = self.ant_location[2]

        if facing == NORTH:
            new_facing = WEST
        if facing == EAST:
            new_facing = NORTH
        if facing == SOUTH:
            new_facing = EAST
        if facing == WEST:
            new_facing = SOUTH

        self.ant_location = (self.ant_location[0], self.ant_location[1], new_facing)

        #return location and view info
        return self._ant_result()


    def ant_rotate_cw(self):
        facing  = self.ant_location[2]

        if facing == NORTH:
            new_facing = EAST
        if facing == EAST:
            new_facing = SOUTH
        if facing == SOUTH:
            new_facing = WEST
        if facing == WEST:
            new_facing = NORTH

        self.ant_location = (self.ant_location[0], self.ant_location[1], new_facing)

        #return location and view info
        return self._ant_result()

    def _convert_ant_facing(self, facing):
        if facing.upper() == "NORTH":
            return NORTH
        elif facing.upper() == "EAST":
            return EAST
        elif facing.upper() == "SOUTH":
            return SOUTH
        elif facing.upper() == "WEST":
            return WEST
        else:
            raise ValueError("Value ''" +facing+ "' for style is not understood")


    def _convert_map_style(self, style_string):
        if style_string.upper() == "BOUNDED":
            return BOUNDED
        elif style_string.upper() == "UNBOUNDED":
            return UNBOUNDED
        else:
            raise ValueError("Value ''" +style_string+ "' for style is not understood")


    def get_ant_view(self):
        facing  = self.ant_location[2]
        position= (self.ant_location[0], self.ant_location[1])

        #sift is a triplet of offsets of left, middle, right view for ant facing
        if facing == NORTH:
            shift = ( (-1,-1), (0,-1), (1,-1) )
        if facing == EAST:
            shift = ( (1,-1), (1,0), (1,1) )
        if facing == SOUTH:
            shift = ( (1,1), (0,1), (-1,1) )
        if facing == WEST:
            shift = ( (-1,1), (-1,0), (-1,-1) )

        #return dict
        return {
            "left":     self._get_offset_pheremone( position, shift[0] ),
            "middle":   self._get_offset_pheremone( position, shift[1] ),
            "right":    self._get_offset_pheremone( position, shift[2] ),
        }


    def _get_offset_pheremone(self, position, offset):
        x = position[0]+offset[0]
        y = position[1]+offset[1]

        #check bounds
        if x < 0 or x >= self.size[0]:
            return None

        if y < 0 or y >= self.size[1]:
            return None

        return self.map[x][y]


    def load_definition(self, map_definition_file):
        try:
            f = open(map_definition_file)
            cfg = json.load(f)

            #configure the map based on the json file
            self.name = cfg["name"]

            self.style = self._convert_map_style(cfg["style"])
            self.size = tuple(cfg["size"])

            #setup the map size
            self.map = list( list( False for _ in range(self.size[1]) )
                for _ in range(self.size[0]))

            #load the trail
            self.trail = cfg["trail"]
            self.trail_len = len(cfg["trail"])
            for pheremone in self.trail:
                self.map[pheremone[0]][pheremone[1]] = True

            #start location
            self.start_location = cfg["start_location"]

            #start location
            self.end_location = cfg["end_location"]

            self.ant_facing = self._convert_ant_facing(cfg["ant_facing"])

            f.close()
            self.loaded = True
            return True

        except FileNotFoundError:
            print("File " + map_definition_file + " not found.")
            return False

        except json.decoder.JSONDecodeError as e:
            print("File " + map_definition_file + " is not a valid JSON file.")
            print(e)
            return False

        except KeyError as e:
            print(e)
            return False

        except ValueError as e:
            print(e)
            return False


    def load_state(self):
        return self.loaded

    def pretty_print(self):
        pprint(self.map)

    def raw_print(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.map[x][y]:
                    if [x,y] == self.start_location:
                        print("@", end="")
                    elif [x,y] == self.end_location:
                        print("#", end="")
                    else:
                        print("*", end="")
                else:
                    print("0", end="")
            print("")

    def reset(self):
        self.ant_location = (self.start_location[0], self.start_location[1],
            self.ant_facing)

        self.trail_pos = 0


if __name__ == "__main__":
    map = AntMap("test/basic_map.json")
    map.raw_print()
