from room import Room
from player import Player
from world import World
from util import Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "projects/adventure/maps/test_line.txt"
# map_file = "projects/adventure/maps/test_cross.txt"
# map_file = "projects/adventure/maps/test_loop.txt"
# map_file = "projects/adventure/maps/test_loop_fork.txt"
map_file = "projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
opposite = {
    "n": "s",
    "s": "n",
    "e": "w",
    "w": "e"
}
visited = set()
available_moves = {}
backtrack = Stack()

visited.add(player.current_room.id)
available_moves[player.current_room.id] = player.current_room.get_exits()
while len(visited) < len(world.rooms) :

    if player.current_room.id not in visited:
        current = player.current_room.id
        visited.add(current)
        available_moves[current] = player.current_room.get_exits()
    while len(available_moves[player.current_room.id]) <= 0:
        go_back = backtrack.pop()
        traversal_path.append(go_back)
        player.travel(go_back)
    go_to = available_moves[player.current_room.id].pop(0)
    traversal_path.append(go_to)
    backtrack.push(opposite[go_to])
    player.travel(go_to)

    # print(backtrack.stack, available_moves)
    # print(traversal_path)
    # break


# WHY IS IT SKIPPING 16???
# for i in range(0, 499):
#     if i not in visited:
#         print(i)
# print(visited)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
