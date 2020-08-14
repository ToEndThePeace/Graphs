from room import Room
from player import Player
from world import World
from util import Stack

import random
import os
from ast import literal_eval


def clear():
    os.system("cls")


def pause(message="Press enter to continue..."):
    input(message)


def traverse_graph(graph):
    """
    traverse_graph takes in a dictionary value that maps rooms numbers to info like so:
        {
            num1: [(x, y), {'e': num2, 'w': num3}]
        }
        where num1 is the room number, and num2/num3 are the room numbers in the
        corresponding cardinal directions on the "map"

    this function uses class methods to figure out how to traverse the "map" so that every
    room is visited at least once
    """
    # load the world and initialize player class
    world = World()
    world.load_graph(graph)
    player = Player(world.starting_room)

    # Print an ASCII map
    world.print_rooms()

    # List to store directions to walk in order to hit every room at least once
    traversal_path = []
    # set to keep track of what rooms we've been in
    visited = set()
    # lookup table for available moves
    available_moves = {}
    # backtrack is like an undo button that lets us go back while maintaining our traversal list
    backtrack = Stack()
    # a simple lookup table to help with our backtrack stack
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

    # TRAVERSAL TEST
    visited_rooms = set()
    player.current_room = world.starting_room
    visited_rooms.add(player.current_room)

    for move in traversal_path:
        player.travel(move)
        visited_rooms.add(player.current_room)

    if len(visited_rooms) == len(graph):
        return f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
    else:
        return f"TESTS FAILED: INCOMPLETE TRAVERSAL\n{len(graph) - len(visited_rooms)} unvisited rooms"


if __name__ == "__main__":
    # clear terminal for clean output
    clear()
    pause("***********************************\n" +
          "*    >   >   ~  -  ~   >   >      *\n" +
          "*  Welcome to the Map Traverser!  *\n" +
          "*    <   <   ~  -  ~   <   <      *\n" +
          "***********************************")
    clear()

    # load all maps given for testing into a list
    maps = ["projects/adventure/maps/test_line.txt",
            "projects/adventure/maps/test_cross.txt",
            "projects/adventure/maps/test_loop.txt",
            "projects/adventure/maps/test_loop_fork.txt",
            "projects/adventure/maps/main_maze.txt"]

    # read the maps into a list of dictionaries
    rooms = [literal_eval(open(map_file, "r").read()) for map_file in maps]

    # run traversal calculation on all given maps
    for i in range(len(rooms)):
        print(f"Running through map {i}...\n")
        res = traverse_graph(rooms[i])
        print("\nTraversal complete!\n")
        print(res + "\n")
        pause()
        clear()

    # cleanup
    clear()
