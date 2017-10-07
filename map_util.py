import numpy as np
import sys
from structs import *
import a_star

class MegaMap:
    def __init__(self):
        self.knownMap = np.zeros((20, 20))
        self.base_position = None
        pass

    def update_map(self, np_map, player_position):
        # type: (np.ndarray, Point)->None
        if self.base_position is None:
            base_position = np.array(player_position - Point(10, 10))
        x = player_position.X - 10
        y = player_position.Y - 10
        np.copyto(self.knownMap[x : x + 20, y : y + 20], np_map)

    def print_all(self):
        for i in xrange(np.shape(self.knownMap)[0]):
            for j in xrange(np.shape(self.knownMap)[1]):
                tile = self.knownMap[i, j]
                if tile == TileType.Tile:
                    sys.stdout.write(" ")
                elif tile == TileType.House:
                    sys.stdout.write("M")
                elif tile == TileType.Lava:
                    sys.stdout.write("~")
                elif tile == TileType.Resource:
                    sys.stdout.write("R")
                elif tile == TileType.Wall:
                    sys.stdout.write("W")
                elif tile == TileType.Shop:
                    sys.stdout.write("S")
                else:
                    sys.stdout.write("X")
            print ""

    def find_path(self, start, dest):
        # type: (Point, Point)->list(Point)
        if dest.X < 0:
            dest.X = 0
        if dest.Y < 0:
            dest.Y = 0
        if dest.X >= self.knownMap.shape[0]:
            dest.X = self.knownMap.shape[0]
        if dest.Y >= self.knownMap.shape[1]:
            dest.Y = self.knownMap.shape[0]

        path = a_star.astar(self.knownMap, (start.X, start.Y), (dest.X, dest.Y))
        if path == False:
            return False
        else:
            return map(lambda x:Point(x[0], x[1]), path)