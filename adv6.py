

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
map_file = "maps/test_loop_fork.txt"
# map_file = "main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

# instance of player class
player = Player(world.starting_room)

# above here: default original code

########################
# # GGA Code
########################

# installing libraries

# setting variables (alphabetical order):
direction_I_want = 'n' # starting out direction
#direction_list = ['n', 's', 'w', 'e']
crossroads_set = set()
crossroads_room_I_want = None
current_room = player.current_room.id
flag__going_in_a_new_direction = True
last_direction = None
my_map = {}
max_room_number = 500
navigation_dict = {}
previous_room = 0  # starting out
reverse_direction_dict = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
room_distance_mask = None
rooms_visited_set = set()
starting_room = 0
step_counter = 0  # ?
this_direction = 'n' # starting out
traversal_path = []
try_going_left = {'n': 'W', 's': 'e', 'e': 'n', 'w': 's'}
try_going_right = {'n': 'e', 's': 'w', 'e': 's', 'w': 'n'}



# for use in checking if you are finished:
# make a list of all existing room numbers, as a set
set_of_all_room_numbers = set([*range(starting_room, max_room_number + 1, 1)])

## Helper Functions Etc.

# portable graph making code

class Queue:
    def __init__(self):
        self.queue = []  # note: change datastruct in future for scale

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)

class Graph:

    """Representize a graph as a dictionary of
        vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}  # This is our adjacency list
        self.cache = {}
        self.raw_data = {}


    def add_dungeon_vertex(self, room_number):
        self.vertices[room_number] = set()


    def add_edge_bidirectional(self, v1, v2):
        """
        Add bi-directional edges to the graph between v1 to v2
        BOTH DIRECTIONS
        """
        # Check if they exist
        if v1 in self.vertices and v2 in self.vertices:
            # Add the edge
            self.vertices[v1].add(v2)
            self.vertices[v2].add(v1)
        else:
            print("ERROR ADDING EDGE: Vertex not found")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        else:
            return None

    def bfs_all_path(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Create a q and enqueue starting vertex
        qq = Queue()
        qq.enqueue([starting_vertex])
        # Create a set of traversed vertices
        visited = []
        # While queue is not empty:
        while qq.size() > 0:
            # dequeue/pop the first vertex
            path = qq.dequeue()
            # if not visited
            if path[-1] not in visited:
                # DO THE THING!!!!!!!
                if path[-1] == destination_vertex:
                    # print("trigger")
                    return path

                # print(path[-1])
                # mark as visited
                visited.extend([path[-1]])
                # enqueue all neightbors
                for next_vert in self.get_neighbors(path[-1]):
                    new_path = list(path)
                    new_path.append(next_vert)
                    qq.enqueue(new_path)
                    
        return visited  # TODO



# this function updates map based on doors in the room you are in
def make_map(current_room):
    if player.current_room.get_exits() == ['n', 's', 'w', 'e']:
        my_map[player.current_room.id] = {'n': '?', 's': '?', 'w': '?', 'e': '?'}

    elif player.current_room.get_exits() == ['n', 's', 'w']:
        my_map[player.current_room.id] = {'n': '?', 's': '?', 'w': '?'}

    elif player.current_room.get_exits() == ['n', 's', 'e']:
        my_map[player.current_room.id] = {'n': '?', 's': '?', 'e': '?'}

    elif player.current_room.get_exits() == ['s', 'w', 'e']:
        my_map[player.current_room.id] = {'s': '?', 'w': '?', 'e': '?'}

    elif player.current_room.get_exits() == ['n', 'w', 'e']:
        my_map[player.current_room.id] = {'n': '?', 'w': '?', 'e': '?'}

    elif player.current_room.get_exits() == ['n', 'e']:
        my_map[player.current_room.id] = {'n': '?', 'e': '?'}

    elif player.current_room.get_exits() == ['n', 'w']:
        my_map[player.current_room.id] = {'n': '?', 'w': '?'}

    elif player.current_room.get_exits() == ['w', 'e']:
        my_map[player.current_room.id] = {'w': '?', 'e': '?'}

    elif player.current_room.get_exits() == ['n', 's']:
        my_map[player.current_room.id] = {'n': '?', 's': '?'}

    elif player.current_room.get_exits() == ['s', 'e']:
        my_map[player.current_room.id] = {'s': '?', 'e': '?'}

    elif player.current_room.get_exits() == ['s', 'w']:
        my_map[player.current_room.id] = {'s': '?', 'w': '?'}

    elif player.current_room.get_exits() == ['n']:
        my_map[player.current_room.id] = {'n': '?'}

    elif player.current_room.get_exits() == ['s']:
        my_map[player.current_room.id] = {'s': '?'}

    elif player.current_room.get_exits() == ['e']:
        my_map[player.current_room.id] = {'e': '?'}

    elif player.current_room.get_exits() == ['w']:
        my_map[player.current_room.id] = {'w': '?'}

    else:
        print("direction choice error")

# boostrap
# instantiation of graph class
dungeon_graph = Graph()
# add starting room
dungeon_graph.add_dungeon_vertex(0)
# add to your map (add your current location)
if current_room not in rooms_visited_set:
    make_map(current_room)
# updated rooms_visited_set
rooms_visited_set.add(0)

# Steps:
# 1. walk in one direction until you hit a dead end (or find a room you found already)
# as you walk, record (somewhere) where options to go a different direction are (intersections)
# 2. if you are at a dead end, go to the nearest cross-roads and go in a new direction.
# 3. record the directions you walked in, as your traversal path.


#####
## Goal: output a compelete traversal_path list
#####

# keep walking until you visit every room:
while rooms_visited_set != set_of_all_room_numbers:

# for testing (just 10 turns)
#for i in range(10):

    # inspection
    print("Taking Another Step...!!!", step_counter)



    ## move:
    ### each time go in a new direction

    ## continue in same direction, unless not an option:
    ## if that's not an option, go back to the nearest 
    ## explored crossroads
    if this_direction not in player.current_room.get_exits():

        # dead end is where you can only go back, try right and left before going to last crossroads.
        
        print("trying right", try_going_right[this_direction])
        print("trying left", try_going_left[this_direction])

        # try going right:
        if try_going_right[this_direction] in player.current_room.get_exits():
            this_direction = try_going_right[this_direction]

        # try going left
        elif try_going_left[this_direction] in player.current_room.get_exits():
            this_direction = try_going_left[this_direction]

        else: # find last crossroads
            print("hit dead end")        
            # start with a blank navidation dict:
            # this will be filled with {distance : room} results
            navigation_dict = {}

            #### Plans
            ## Since you hit a dead end, find the closest path back to the nearest
            ## unexplored crossroads:
            ## check distance to each room on your crossraods list
            ## which rooms contain unexplored crossroads?
            ## check map-room-dictionaries for question-marks

            #print("crossroads_set1", crossroads_set)
            #print("rooms_visited_set1", rooms_visited_set)        

            # Step
            # check which room in the crossroads set is closest
            # keep track of distances
            # using a navigation dictionary
            # {lenth of path : which room that is to}

            for this_room_id in crossroads_set:

                # using mask for readability
                # remove current room from path to next room
                room_distance_mask = len(dungeon_graph.bfs_all_path(current_room, this_room_id)[1:])

                # inspection
                #print("room_distance_mask", room_distance_mask)
                #print("full path", dungeon_graph.bfs_all_path(current_room, this_room_id))

                # make entry in navigation_dict
                # {lenth of path : which room that is to}
                navigation_dict[room_distance_mask] = this_room_id

            # Find the direction you want
            # the direction you want is:
            # the direction to (n,w,e,s)
            # the smallest (min) number 
            # in list of keys (distances) in your distance dictionary
            # hence: crossroads_room_I_want = the closest such room
            mask_min_distance = min(list(navigation_dict.keys()))
            crossroads_room_I_want = navigation_dict[mask_min_distance]

            print("crossroads_room_I_want:", crossroads_room_I_want)
            print("I am here now:", player.current_room.id)
            print("BFS path", dungeon_graph.bfs_all_path(current_room, crossroads_room_I_want))

            # step: quickmarch
            # quickmarch all the steps to that crossroads
            # follow each step in traversal list, and add that step
            # to your traversal_path
            # each pass though this while loop takes one step closer
            while player.current_room.id != crossroads_room_I_want:
                # # inspection
                # print("quickmarch current room 1", player.current_room.id)
                # print("crossroads_room_I_want", crossroads_room_I_want)
                # print("path", dungeon_graph.bfs_all_path(current_room, crossroads_room_I_want))

                # get id of the next_room_along_the_way
                # note: the 'first' [0] room is the current room
                # so you want the 2nd room [1]
                next_room_along_the_way = dungeon_graph.bfs_all_path(player.current_room.id, crossroads_room_I_want)[1]

                # get directions to go to that room from current_room
                # make a mask:
                here = my_map[player.current_room.id]
                # reverse (value -> key) lookup of which direction the next room is in:
                new_direction = list(here.keys())[list(here.values()).index(next_room_along_the_way)]

                # # inspection
                # print("moving to new room")
                # print(player.current_room.id)

                # go in that direction
                player.travel(new_direction)

                ######
                ## Moved to New Room
                ######

                # # inspection
                # print(player.current_room.id)

                # Update Lists Maps and Variables:
                # record your traversal path
                traversal_path.extend([new_direction])
                # update rooms
                # where you were
                previous_room = current_room
                # where you are
                current_room = player.current_room.id
                
                # # # inspection
                # print("quickmarch current room 1", current_room)
                # print("crossroads_room_I_want",crossroads_room_I_want)
                # print("crossroads_set", crossroads_set)

                step_counter += 1

            # TODO: where should this be?
            # then, in the new room: pick a new direction
            direction_to_try = random.choice(player.current_room.get_exits())
            while my_map[current_room][direction_to_try] != '?':
                direction_to_try = random.choice(player.current_room.get_exits())
            # update 'this direction' 
            this_direction = direction_to_try



    else: # if you can keep going int he same direction
        # go in that direction
        player.travel(this_direction)


    #####
    ## New Room
    #####

    # update rooms
    # where you were
    previous_room = current_room
    # where you are
    current_room = player.current_room.id

    # add to your map (add your current location)
    if current_room not in rooms_visited_set:
        make_map(current_room)

    # add new room to the graph
    dungeon_graph.add_dungeon_vertex(player.current_room.id)

    # update edges on maps:
    # print(current_room, previous_room)
    dungeon_graph.add_edge_bidirectional(current_room, previous_room)

    # record your traversal path
    traversal_path.extend([this_direction])

    # # Step: update '?' in map for cross-roads
    # e.g. each time you go to a new room:
    # 1. the last room should be updated to include the new room
    my_map[previous_room][this_direction] = player.current_room.id

    # 2. the new room should be updated to include the old room   
    # use reverse direction to update 
    # the current room "backwards" to the last room
    my_map[current_room][reverse_direction_dict[this_direction]] = previous_room

    # update direction variables
    last_direction = this_direction

    # updated rooms_visited_set
    rooms_visited_set.add(player.current_room.id)

    # Step
    # iterate through rooms_visited_set
    # looking for a '?', 
    # signifying unexplored crossroads
    #reset_crossroads
    crossroads_set = set()
    for room_id in rooms_visited_set:
        # for visited room each room, check for '?'
        if '?' in list(my_map[room_id].values()):
            # if '?' is found, add that room
            # to the new crossroads_set 
            crossroads_set.add(room_id)

    step_counter += 1

    # display data
    print("data from end of move: \n")
    print("this room", current_room)
    print("this room", traversal_path)
    print("my map", my_map)
    print("this_direction", this_direction)
    print("rooms_visited_set", rooms_visited_set)
    print("crossroads_set", crossroads_set)
    print("path:", traversal_path)
    print("nodes", dungeon_graph.vertices)
    print(" \n")

    # for testing
    #break

# Fill this out with directions to walk
# traversal_path = []



###########################################

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
#player.current_room.print_room_description(player)

## to walk around
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
