from room import Room
from player import Player
from world import World

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
previous_room = None

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

def next_direction(room):
    possible_directions = []
    if "?" in rooms[room.id].values():
        for connection in rooms[room.id]:
            if rooms[room.id][connection] == '?':
                possible_directions.append(connection)
    else:
        possible_directions = list(rooms[room.id].keys())
    return random.choice(possible_directions)

def edit_connection(next_room, previous_room):
    rooms[previous_room.id][direction] = next_room.id
    opposite = opposite_direction(direction)
    rooms[next_room.id][opposite] = previous_room.id

def find_last_unexhausted_room(current_room):
    room = current_room
    distance_to_room = -1
    directions_to_append = []
    while '?' not in rooms[room.id].values():
        if abs(distance_to_room) >= len(traversal_path):
            break
        previous_direction = traversal_path[distance_to_room]
        opposite = opposite_direction(previous_direction)
        directions_to_append.append(opposite)
        room = room.get_room_in_direction(opposite)
        distance_to_room -= 1
    traversal_path.extend(directions_to_append)
    return room

# Set initial room's directions entry
set_room_directions(current_room)

# Start main section
# Loop through until short enough path is found
while True:
    traversal_path = []
    visited = set()
    current_room = world.starting_room

    # Loop til all rooms have been traversed
    while len(visited) < len(room_graph):
        # Add to visited
        visited.add(current_room)

        # Test if room has any untravelled connections
        if '?' not in rooms[current_room.id].values():
            current_room = find_last_unexhausted_room(current_room)
            continue

        # Set direction
        direction = next_direction(current_room)
        traversal_path.append(direction)

        # Set previous room to current room and current room to next room
        previous_room = current_room
        current_room = current_room.get_room_in_direction(direction)

        # Set next room's directions entry
        set_room_directions(current_room)

        # Set connections between previous room and next room
        edit_connection(current_room, previous_room)

    print(len(traversal_path))
    if len(traversal_path) < 2000:
        break


# while len(visited) < len(room_graph):
#     exits = current_room.get_exits()
#     if len(traversal_path) > 0 and len(exits) > 1:
#         exits.remove(opposite_direction(traversal_path[-1]))
#     direction = random.choice(exits)
#     traversal_path.append(direction)
#     visited.add(current_room.id)
#     current_room = current_room.get_room_in_direction(direction)
#





traversal_path.pop()




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
