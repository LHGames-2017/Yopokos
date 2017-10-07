from flask import Flask, request
from structs import *
import json
import numpy as np
import sys
import a_star
import operator

app = Flask(__name__)

def create_action(action_type, target):
    actionContent = ActionContent(action_type, target.__dict__)
    return json.dumps(actionContent.__dict__)

def create_move_action(target):
    return create_action("MoveAction", target)

def create_attack_action(target):
    return create_action("AttackAction", target)

def create_collect_action(target):
    return create_action("CollectAction", target)

def create_steal_action(target):
    return create_action("StealAction", target)

def create_heal_action():
    return create_action("HealAction", "")

def create_purchase_action(item):
    return create_action("PurchaseAction", item)

def deserialize_map(serialized_map):
    """
    Fonction utilitaire pour comprendre la map
    """
    serialized_map = serialized_map[1:]
    rows = serialized_map.split('[')
    column = rows[0].split('{')
    deserialized_map = [[Tile() for x in xrange(20)] for y in xrange(20)]
    for i in range(len(rows) - 1):
        column = rows[i + 1].split('{')

        for j in range(len(column) - 1):
            infos = column[j + 1].split(',')
            end_index = infos[2].find('}')
            content = int(infos[0])
            x = int(infos[1])
            y = int(infos[2][:end_index])
            deserialized_map[i][j] = Tile(content, x, y)

    return deserialized_map

def map_to_np(map):
    npmap = np.zeros((len(map), len(map[0])))
    for x, line in enumerate(map):
        for y, tile in enumerate(line):
            npmap[x, y] = int(tile.Content)
    return npmap

def printMap(map):
    for i in xrange(len(map)):
        for j in xrange(len(map[i])):
            tile = map[i][j].Content
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

def get_shortest_move_to_resources(map, target_pos_array):
    # type: (np.ndarray, list(Point))->tuple(int, int)
    paths = []
    for target_pos in target_pos_array:
        paths.append(get_move_to(map, target_pos))
    min_index, min_value = min(enumerate(paths), key=operator.itemgetter(1))

    return paths[min_index][-1]


def get_move_to(map, target_pos):
    # type: (np.ndarray, Point, Point)->list(tuple(int, int))
    path = a_star.astar(map, (10, 10), (target_pos.X, target_pos.Y))
    return path

def bot():
    """
    Main de votre bot.
    """
    map_json = request.form["map"]

    #map_json = json.loads(encoded_map)

    #print map_json

    #return create_move_action(Point(0,1))

    # Player info

    #encoded_map = map_json.encode()
    map_json = json.loads(map_json)
    p = map_json["Player"]
    pos = p["Position"]
    x = pos["X"]
    y = pos["Y"]
    house = p["HouseLocation"]
    player = Player(p["Health"], p["MaxHealth"], Point(x,y),
                    Point(house["X"], house["Y"]),
                    0,
                    p["CarriedResources"], p["CarryingCapacity"])

    # Map
    serialized_map = map_json["CustomSerializedMap"]
    deserialized_map = deserialize_map(serialized_map)

    #print deserialized_map
    npmap = map_to_np(deserialized_map)
    printMap(deserialized_map)

    otherPlayers = []
    """
    for player_dict in map_json["OtherPlayers"]:
        for player_name in player_dict.keys():
            player_info = player_dict[player_name]
            p_pos = player_info["Position"]
            player_info = PlayerInfo(player_info["Health"],
                                     player_info["MaxHealth"],
                                     Point(p_pos["X"], p_pos["Y"]))

            otherPlayers.append({player_name: player_info })
    """

    print get_move_to(npmap, Point(18,13))
    # return decision
    return create_move_action(Point(player.Position.X,player.Position.Y))

@app.route("/", methods=["POST"])
def reponse():
    """
    Point d'entree appelle par le GameServer
    """
    res = bot()
    print res
    return res

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
