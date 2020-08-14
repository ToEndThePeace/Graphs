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
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# set to keep track of what rooms we've been in
visited = set()
# lookup table for available moves
available_moves = {}
# to store a backwards
backtrack = Stack()
opposite = {
    "n": "s",
    "s": "n",
    "e": "w",
    "w": "e"
}

# initialize lookup tables to remedy backtrack removal indexing issue
visited.add(player.current_room.id)
available_moves[player.current_room.id] = player.current_room.get_exits()

# loop until we've visited EVERY room
while len(visited) < len(world.rooms) - 1:

    # if player.current_room.id in visited:
    # this sets up our lookup tables on first encounter!
    if player.current_room.id not in visited:
        # get the current room id to use as index in visited set and available_moves lookup table
        current = player.current_room.id
        visited.add(current)
        # we only call get_exits ONCE PER ROOM so that we know when we've already gone somewhere!
        available_moves[current] = player.current_room.get_exits()
        # because traversing between rooms is UNDIRECTED, if you go north from room 1 to room 2,
        # you don't need to go south from room 2~~
        # adding initialization statements before the outer while loop to prevent indexing issue
        available_moves[player.current_room.id].remove(backtrack.stack[-1])

    # when we've gone down ever corridor in our current room already, backtrack!~
    while len(available_moves[player.current_room.id]) <= 0:
        # get the step to backtrack to the last room we were in
        go_back = backtrack.pop()
        # add it to our traversal path
        traversal_path.append(go_back)
        # and then go there
        player.travel(go_back)

    # check available moves for our next step (and REMOVE that move from our lookup table!),
    # add to traversal path, and go there!
    go_to = available_moves[player.current_room.id].pop()
    traversal_path.append(go_to)
    player.travel(go_to)

    # store the reverse of the direction in our backtrack stack, so we know where to go
    # when we run out of available moves in our current room
    backtrack.push(opposite[go_to])

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
