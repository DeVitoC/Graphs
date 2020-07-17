from room import Room
from player import Player
from world import World
from collections import deque

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = set()
rooms = {}
current_room = world.starting_room
stack = deque()

# Returns the opposite direction to the passed direction
def opposite_direction(direction):
    if direction == "n":
        return "s"
    elif direction == "s":
        return "n"
    elif direction == "e":
        return "w"
    elif direction == "w":
        return "e"

#
def set_room_directions(room):
    exits = room.get_exits()
    rooms[room.id] = {}
    for exit in exits:
        rooms[room.id][exit] = "?"

# while True:
#     traversal_path = []
#     visited = set()
#     rooms = {}
#     player.current_room = world.starting_room
#     stack = deque()
# Set initial room's directions entry
set_room_directions(current_room)

while len(visited) < 500:
    # Set current room to player.current_room
    current_room = player.current_room
    # Add current room to visited
    visited.add(current_room)
    # Get neighboring rooms
    possible_rooms = rooms[current_room.id]
    # Create empty list to store neighboring rooms not visited
    not_visited = []
    # Add exits that have not been explored to not_visited array
    for exit in current_room.get_exits():
        if possible_rooms[exit] == '?':
            not_visited.append(exit)
    # If any exits are not visited, add to stack and traversal_path, and travel in first direction not visited already
    if len(not_visited) > 0:
        player.travel(not_visited[0])
        stack.append(not_visited[0] )
        traversal_path.append(not_visited[0])
        # If current_room not in rooms dictionary, add to dictionary
        if player.current_room.id not in rooms:
            set_room_directions(player.current_room)
        # Set new connections
        rooms[player.current_room.id][opposite_direction(not_visited[0])] = current_room.id
        rooms[current_room.id][not_visited[0]] = player.current_room.id
    # Otherwise, if stack has rooms, travel back a room
    else:
        if len(stack) > 0:
            last_direction = stack.pop()
            opposite = opposite_direction(last_direction)
            player.travel(opposite)
            traversal_path.append(opposite)





traversal_path.pop()
print(len(traversal_path))
print(traversal_path)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
