

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
map_file = "main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

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
edges_dict = {}  # Alt for testing
my_map = {}
my_map2 = {}  # Alt for testing
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
try_going_left = {'n': 'w', 's': 'e', 'e': 'n', 'w': 's'}
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

    def add_vertex_number(self, number):
        """
        Add a vertex to the graph.
        """
        for room_number in range(0, number):
            self.vertices[room_number] = set()


    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_dungeon_vertex(self, room_number):
        self.vertices[room_number] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph from v1 to v2
        """
        # Check if they exist
        if v1 in self.vertices and v2 in self.vertices:
            # Add the edge
            self.vertices[v1].add(v2)
            self.vertices[v2].add(v1)
        else:
            print("ERROR ADDING EDGE: Vertex not found")

    def add_one_edge(self, v1, v2):
        """
        Add a directed edge to the graph from v1 to v2
        """
        # Check if they exist
        if v1 in self.vertices and v2 in self.vertices:
            # Add the edge
            self.vertices[v1].add(v2)
        else:
            print("ERROR ADDING EDGE: Vertex not found")

    def add_edge_bidirectional(self, v1, v2):
        """
        Add bi-directional edges to the graph between v1 to v2
        BOTH DIRECTIONS
        """
        # Check if they exist
        if v1 in self.vertices and v2 in self.vertices:
            # Add the edges
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

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Create a q and enqueue starting vertex
        qq = Queue()
        qq.enqueue([starting_vertex])
        # Create a set of traversed vertices
        visited = set()
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
                visited.add(path[-1])
                # enqueue all neightbors
                for next_vert in self.get_neighbors(path[-1]):
                    new_path = list(path)
                    new_path.append(next_vert)
                    qq.enqueue(new_path)
        pass  # TODO

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

edges_dict = {0: {8, 1, 3, 4}, 1: {0, 2, 22, 7}, 2: {1, 10, 5}, 3: {0, 11, 21}, 4: {0}, 5: {2, 50, 6}, 6: {5, 62, 23}, 7: {1, 12, 9}, 8: {0, 16}, 9: {13, 7}, 10: {2, 38}, 11: {80, 3}, 12: {18, 20, 7}, 13: {9, 14, 15}, 14: {17, 13, 47}, 15: {19, 13}, 16: {8}, 17: {46, 33, 28, 14}, 18: {24, 34, 12}, 19: {32, 40, 15}, 20: {26, 12, 31}, 21: {3, 36}, 22: {1}, 23: {57, 58, 6}, 24: {25, 18, 29}, 25: {24, 43}, 26: {27, 20}, 27: {26, 55}, 28: {17, 60, 30}, 29: {24, 54}, 30: {28}, 31: {20, 37}, 32: {19}, 33: {17}, 34: {18, 35, 39}, 35: {34, 44}, 36: {41, 21}, 37: {42, 91, 31}, 38: {10}, 39: {34, 52, 71}, 40: {74, 19, 45}, 41: {36, 69, 76}, 42: {51, 37}, 43: {25, 77, 49}, 44: {48, 59, 35}, 45: {40, 81, 85}, 46: {17, 61, 79}, 47: {14}, 48: {44, 53}, 49: {43, 119}, 50: {66, 5, 70}, 51: {42, 93}, 52: {39}, 53: {48, 75}, 54: {29}, 55: {56, 27}, 56: {73, 67, 55}, 57: {68, 94, 23}, 58: {23}, 59: {44, 189}, 60: {64, 28}, 61: {82, 46, 63}, 62: {65, 6}, 63: {140, 61}, 64: {60, 102, 111}, 65: {134, 62}, 66: {96, 50}, 67: {56, 84}, 68: {57}, 69: {72, 41}, 70: {50, 116, 87}, 71: {115, 150, 39}, 72: {89, 69}, 73: {56, 132}, 74: {40}, 75: {88, 53, 78}, 76: {41}, 77: {130, 43}, 78: {90, 75}, 79: {106, 46}, 80: {83, 11}, 81: {108, 137, 92, 45}, 82: {155, 61}, 83: {80, 99}, 84: {67, 86}, 85: {45}, 86: {146, 84, 95}, 87: {117, 70}, 88: {75, 125, 103}, 89: {72, 104}, 90: {98, 142, 78}, 91: {101, 37}, 92: {128, 81, 100}, 93: {51}, 94: {57, 97, 113}, 95: {109, 86}, 96: {66, 179}, 97: {153, 110, 94}, 98: {186, 90}, 99: {122, 83}, 100: {92}, 101: {91}, 102: {64, 107}, 103: {88}, 104: {89, 126, 105}, 105: {104, 129, 225}, 106: {112, 161, 79}, 107: {141, 102}, 108: {81, 167}, 109: {136, 95}, 110: {97, 157, 118}, 111: {64, 121, 114}, 112: {210, 106, 124}, 113: {145, 94}, 114: {120, 111}, 115: {160, 71}, 116: {70, 159}, 117: {170, 127, 87}, 118: {218, 133, 110}, 119: {49, 219, 131}, 120: {114}, 121: {123, 148, 111}, 122: {99}, 123: {121, 138}, 124: {112, 174}, 125: {88, 198, 238}, 126: {104, 158, 135}, 127: {212, 117, 173}, 128: {194, 162, 92}, 129: {105, 190}, 130: {77}, 131: {329, 119}, 132: {73, 172}, 133: {234, 118, 151}, 134: {144, 65}, 135: {149, 126}, 136: {109, 231}, 137: {168, 81}, 138: {123, 139, 143}, 139: {176, 138, 147}, 140: {63}, 141: {107, 175}, 142: {90, 245}, 143: {138}, 144: {218, 134}, 145: {113, 183}, 146: {86}, 147: {152, 154, 139}, 148: {121, 178, 163}, 149: {191, 156, 135}, 150: {251, 71}, 151: {188, 133}, 152: {233, 147, 196}, 153: {97}, 154: {192, 147, 184}, 155: {185, 82}, 156: {209, 177, 149}, 157: {110}, 158: {235, 164, 126}, 159: {116}, 160: {115, 214}, 161: {106, 166}, 162: {128, 205}, 163: {257, 148, 228, 165}, 164: {180, 158}, 165: {169, 163, 197}, 166: {208, 161}, 167: {187, 108}, 168: {137, 171, 207}, 169: {385, 165, 223}, 170: {117, 182}, 171: {168}, 172: {132}, 173: {202, 127}, 174: {221, 124, 277}, 175: {200, 141}, 176: {139}, 177: {156, 215}, 178: {148}, 179: {96, 201, 181}, 180: {164}, 181: {179}, 182: {170, 211}, 183: {145}, 184: {154}, 185: {155, 292, 195}, 186: {98, 262}, 187: {301, 303, 167}, 188: {151}, 189: {275, 59}, 190: {129, 222}, 191: {193, 149}, 192: {154, 239}, 193: {241, 203, 191}, 194: {128, 227}, 195: {185}, 196: {152, 224, 278}, 197: {165, 199}, 198: {125, 270}, 199: {281, 197, 318}, 200: {328, 204, 175}, 201: {179, 206}, 202: {249, 267, 173}, 203: {193, 269}, 204: {200}, 205: {162, 254}, 206: {232, 201}, 207: {168, 297}, 208: {307, 166}, 209: {156, 213}, 210: {112}, 211: {248, 182}, 212: {229, 127}, 213: {216, 209, 217}, 214: {160, 246}, 215: {177, 243, 220}, 216: {236, 213}, 217: {213, 271}, 218: {144, 252, 118}, 219: {305, 242, 119}, 220: {314, 230, 215}, 221: {342, 250, 174}, 222: {274, 190}, 223: {169, 483}, 224: {196, 287}, 225: {105, 226}, 226: {225, 260}, 227: {194}, 228: {163, 253}, 229: {212, 237}, 230: {344, 220}, 231: {136, 282, 294}, 232: {265, 244, 206}, 233: {152, 240}, 234: {280, 259, 133, 247}, 235: {158}, 236: {216, 258, 263}, 237: {370, 229}, 238: {381, 293, 125}, 239: {192, 336, 255}, 240: {304, 233}, 241: {256, 193}, 242: {219, 286}, 243: {215}, 244: {232, 264}, 245: {142, 343}, 246: {412, 325, 214}, 247: {369, 234}, 248: {272, 211}, 249: {202}, 250: {289, 221, 295}, 251: {150}, 252: {218, 261}, 253: {228, 285}, 254: {284, 205}, 255: {239}, 256: {241, 327, 279}, 257: {163, 388}, 258: {236}, 259: {234, 291}, 260: {226, 266}, 261: {345, 252}, 262: {186, 390}, 263: {372, 299, 236}, 264: {290, 244}, 265: {232, 273, 268}, 266: {379, 260}, 267: {202, 302}, 268: {265, 276}, 269: {315, 203}, 270: {300, 198}, 271: {217, 310}, 272: {248}, 273: {296, 265, 298}, 274: {222}, 275: {283, 189}, 276: {322, 459, 268}, 277: {331, 174}, 278: {338, 196}, 279: {256, 323}, 280: {234}, 281: {392, 350, 199}, 282: {231}, 283: {376, 275}, 284: {368, 349, 470, 254}, 285: {253}, 286: {288, 242, 309}, 287: {224, 313, 353}, 288: {326, 498, 286}, 289: {250, 324, 319}, 290: {264}, 291: {306, 259}, 292: {185, 316}, 293: {238}, 294: {363, 311, 231}, 295: {250, 332}, 296: {273, 308, 382}, 297: {207}, 298: {360, 273}, 299: {312, 356, 263}, 300: {320, 270}, 301: {187}, 302: {402, 267}, 303: {352, 187, 333}, 304: {240, 321}, 305: {330, 219}, 306: {291, 415}, 307: {208}, 308: {296, 337, 317}, 309: {377, 371, 286}, 310: {271}, 311: {499, 389, 294}, 312: {355, 347, 299}, 313: {287}, 314: {339, 220}, 315: {269, 406, 335}, 316: {292, 341}, 317: {416, 308}, 318: {394, 340, 199}, 319: {289, 441}, 320: {300, 471}, 321: {304, 354, 334}, 322: {424, 276}, 323: {279}, 324: {289, 411, 391}, 325: {246}, 326: {288}, 327: {256, 362}, 328: {200}, 329: {131, 407}, 330: {305, 348, 454}, 331: {387, 277}, 332: {351, 295}, 333: {365, 358, 303}, 334: {384, 321}, 335: {346, 315, 378}, 336: {421, 373, 239}, 337: {308, 383}, 338: {278}, 339: {314, 404}, 340: {374, 318}, 341: {316}, 342: {357, 221}, 343: {245}, 344: {367, 230, 359}, 345: {409, 261}, 346: {335}, 347: {312, 437, 375}, 348: {330}, 349: {418, 284}, 350: {281, 425}, 351: {417, 332, 453}, 352: {303}, 353: {380, 287}, 354: {321, 386, 361}, 355: {312, 457}, 356: {299, 405}, 357: {342}, 358: {333, 397, 399}, 359: {344, 458}, 360: {298, 364}, 361: {354, 366}, 362: {395, 469, 327}, 363: {294}, 364: {360, 401}, 365: {333, 414, 447}, 366: {361, 497}, 367: {344, 462}, 368: {465, 436, 284}, 369: {247}, 370: {237}, 371: {309, 430}, 372: {433, 263}, 373: {336}, 374: {340}, 375: {393, 347, 413}, 376: {283, 468}, 377: {456, 309}, 378: {466, 335}, 379: {266}, 380: {353, 476, 445}, 381: {238, 431}, 382: {296, 455}, 383: {337, 460}, 384: {435, 334}, 385: {169}, 386: {354, 388}, 387: {331, 444}, 388: {257, 386}, 389: {311}, 390: {398, 262}, 391: {489, 324, 396}, 392: {408, 281}, 393: {375}, 394: {426, 422, 318}, 395: {362, 423}, 396: {391}, 397: {358}, 398: {390, 487}, 399: {400, 358}, 400: {492, 399}, 401: {420, 427, 364}, 402: {403, 302}, 403: {402, 439}, 404: {482, 339}, 405: {432, 356}, 406: {410, 315}, 407: {329}, 408: {392, 443}, 409: {488, 345}, 410: {406}, 411: {428, 324}, 412: {246}, 413: {419, 478, 375}, 414: {365}, 415: {306}, 416: {317}, 417: {442, 351}, 418: {463, 349, 479}, 419: {413}, 420: {464, 401}, 421: {336}, 422: {394, 461}, 423: {395}, 424: {322}, 425: {434, 350}, 426: {394}, 427: {401, 474, 438}, 428: {411, 452, 429}, 429: {451, 428}, 430: {440, 371}, 431: {381}, 432: {449, 473, 405}, 433: {372}, 434: {425}, 435: {384}, 436: {368}, 437: {347}, 438: {448, 427}, 439: {403}, 440: {430}, 441: {319}, 442: {417}, 443: {408, 477}, 444: {387}, 445: {480, 380, 446}, 446: {445}, 447: {365}, 448: {490, 475, 438}, 449: {432, 450}, 450: {449}, 451: {429}, 452: {428}, 453: {351}, 454: {330}, 455: {382}, 456: {377}, 457: {355, 494}, 458: {463, 359}, 459: {467, 276}, 460: {383}, 461: {422}, 462: {486, 367}, 463: {458, 418}, 464: {420}, 465: {368}, 466: {472, 378}, 467: {459}, 468: {376}, 469: {362}, 470: {284}, 471: {320}, 472: {481, 466, 495}, 473: {432}, 474: {427}, 475: {448, 496}, 476: {380}, 477: {443}, 478: {493, 413}, 479: {418}, 480: {445}, 481: {472, 485}, 482: {404, 484}, 483: {223}, 484: {482}, 485: {481}, 486: {462}, 487: {398}, 488: {409}, 489: {491, 391}, 490: {448}, 491: {489}, 492: {400}, 493: {478}, 494: {457}, 495: {472}, 496: {475}, 497: {366}, 498: {288}, 499: {311}}
my_map2 = {494: {'e': 457}, 492: {'e': 400}, 493: {'e': 478}, 457: {'e': 355, 'w': 494}, 484: {'n': 482}, 482: {'s': 484, 'e': 404}, 486: {'e': 462}, 479: {'e': 418}, 465: {'e': 368}, 414: {'e': 365}, 400: {'e': 399, 'w': 492}, 451: {'e': 429}, 452: {'e': 428}, 478: {'e': 413, 'w': 493}, 393: {'e': 375}, 437: {'e': 347}, 355: {'e': 312, 'w': 457}, 433: {'e': 372}, 404: {'n': 339, 'w': 482}, 339: {'s': 404, 'e': 314}, 367: {'n': 462, 'e': 344}, 462: {'s': 367, 'w': 486}, 463: {'e': 458, 'n': 418}, 418: {'e': 349, 'w': 479, 's': 463}, 368: {'n': 436, 'e': 284, 'w': 465}, 436: {'s': 368}, 447: {'n': 365}, 365: {'s': 447, 'e': 333, 'w': 414}, 399: {'e': 358, 'w': 400}, 429: {'n': 428, 'w': 451}, 428: {'s': 429, 'e': 411, 'w': 452}, 419: {'n': 413}, 413: {'n': 375, 's': 419, 'w': 478}, 375: {'n': 347, 's': 413, 'w': 393}, 347: {'n': 312, 's': 375, 'w': 437}, 312: {'s': 347, 'e': 299, 'w': 355}, 372: {'e': 263, 'w': 433}, 258: {'e': 236}, 314: {'e': 220, 'w': 339}, 344: {'n': 359, 'e': 230, 'w': 367}, 359: {'n': 458, 's': 344}, 458: {'s': 359, 'w': 463}, 349: {'n': 284, 'w': 418}, 284: {'n': 470, 's': 349, 'e': 254, 'w': 368}, 470: {'s': 284}, 301: {'e': 187}, 333: {'n': 358, 'e': 303, 'w': 365}, 358: {'n': 397, 's': 333, 'w': 399}, 397: {'s': 358}, 411: {'e': 324, 'w': 428}, 396: {'e': 391}, 449: {'n': 432, 'e': 450}, 432: {'n': 405, 's': 449, 'e': 473}, 405: {'n': 356, 's': 432}, 356: {'n': 299, 's': 405}, 299: {'n': 263, 's': 356, 'w': 312}, 263: {'n': 236, 's': 299, 'w': 372}, 236: {'s': 263, 'e': 216, 'w': 258}, 220: {'n': 230, 'e': 215, 'w': 314}, 230: {'s': 220, 'w': 344}, 266: {'n': 379, 'e': 260}, 379: {'s': 266}, 274: {'e': 222}, 254: {'e': 205, 'w': 284}, 227: {'e': 194}, 187: {'n': 303, 'e': 167, 'w': 301}, 303: {'n': 352, 's': 187, 'w': 333}, 352: {'s': 303}, 357: {'e': 342}, 324: {'n': 391, 'e': 289, 'w': 411}, 391: {'n': 489, 's': 324, 'w': 396}, 489: {'n': 491, 's': 391}, 491: {'s': 489}, 450: {'w': 449}, 473: {'w': 432}, 423: {'e': 395}, 469: {'e': 362}, 310: {'n': 271}, 271: {'s': 310, 'e': 217}, 216: {'e': 213, 'w': 236}, 215: {'n': 243, 'e': 177, 'w': 220}, 243: {'s': 215}, 260: {'n': 226, 'w': 266}, 226: {'s': 260, 'e': 225}, 222: {'e': 190, 'w': 274}, 205: {'e': 162, 'w': 254}, 194: {'e': 128, 'w': 227}, 167: {'e': 108, 'w': 187}, 171: {'e': 168}, 297: {'e': 207}, 342: {'e': 221, 'w': 357}, 289: {'n': 319, 'e': 250, 'w': 324}, 319: {'n': 441, 's': 289}, 441: {'s': 319}, 453: {'e': 351}, 395: {'n': 362, 'w': 423}, 362: {'n': 327, 's': 395, 'w': 469}, 327: {'s': 362, 'e': 256}, 217: {'n': 213, 'w': 271}, 213: {'s': 217, 'e': 209, 'w': 216}, 177: {'e': 156, 'w': 215}, 180: {'e': 164}, 235: {'e': 158}, 225: {'e': 105, 'w': 226}, 190: {'e': 129, 'w': 222}, 162: {'n': 128, 'w': 205}, 128: {'s': 162, 'e': 92, 'w': 194}, 108: {'e': 81, 'w': 167}, 168: {'n': 207, 'e': 137, 'w': 171}, 207: {'s': 168, 'w': 297}, 221: {'n': 250, 'e': 174, 'w': 342}, 250: {'n': 295, 's': 221, 'w': 289}, 295: {'n': 332, 's': 250}, 332: {'n': 351, 's': 295}, 351: {'n': 417, 's': 332, 'w': 453}, 417: {'n': 442, 's': 351}, 442: {'s': 417}, 410: {'e': 406}, 323: {'n': 279}, 279: {'n': 256, 's': 323}, 256: {'n': 241, 's': 279, 'w': 327}, 241: {'s': 256, 'e': 193}, 209: {'n': 156, 'w': 213}, 156: {'s': 209, 'e': 149, 'w': 177}, 164: {'n': 158, 'w': 180}, 158: {'s': 164, 'e': 126, 'w': 235}, 105: {'n': 129, 'e': 104, 'w': 225}, 129: {'s': 105, 'w': 190}, 100: {'n': 92}, 92: {'n': 81, 's': 100, 'w': 128}, 81: {'n': 137, 's': 92, 'e': 45, 'w': 108}, 137: {'s': 81, 'w': 168}, 124: {'n': 174, 'e': 112}, 174: {'n': 277, 's': 124, 'w': 221}, 277: {'n': 331, 's': 174}, 331: {'n': 387, 's': 277}, 387: {'n': 444, 's': 331}, 444: {'s': 387}, 422: {'n': 461, 'e': 394}, 461: {'s': 422}, 406: {'n': 315, 'w': 410}, 315: {'n': 269, 's': 406, 'e': 335}, 269: {'n': 203, 's': 315}, 203: {'n': 193, 's': 269}, 193: {'n': 191, 's': 203, 'w': 241}, 191: {'n': 149, 's': 193}, 149: {'n': 135, 's': 191, 'w': 156}, 135: {'n': 126, 's': 149}, 126: {'n': 104, 's': 135, 'w': 158}, 104: {'n': 89, 's': 126, 'w': 105}, 89: {'n': 72, 's': 104}, 72: {'n': 69, 's': 89}, 69: {'s': 72, 'e': 41}, 45: {'n': 85, 'e': 40, 'w': 81}, 85: {'s': 45}, 112: {'n': 210, 'e': 106, 'w': 124}, 210: {'s': 112}, 208: {'n': 307, 'e': 166}, 307: {'s': 208}, 341: {'e': 316}, 374: {'e': 340}, 394: {'n': 426, 'e': 318, 'w': 422}, 426: {'s': 394}, 477: {'e': 443}, 485: {'e': 481}, 346: {'n': 335}, 335: {'s': 346, 'e': 378, 'w': 315}, 369: {'n': 247}, 247: {'s': 369, 'e': 234}, 151: {'n': 188, 'e': 133}, 188: {'s': 151}, 183: {'n': 145}, 145: {'s': 183, 'e': 113}, 122: {'n': 99}, 99: {'n': 83, 's': 122}, 83: {'s': 99, 'e': 80}, 76: {'n': 41}, 41: {'s': 76, 'e': 36, 'w': 69}, 40: {'n': 74, 'e': 19, 'w': 45}, 74: {'s': 40}, 106: {'n': 161, 'e': 79, 'w': 112}, 161: {'n': 166, 's': 106}, 166: {'s': 161, 'w': 208}, 292: {'n': 316, 'e': 185}, 316: {'s': 292, 'w': 341}, 340: {'n': 318, 'w': 374}, 318: {'s': 340, 'e': 199, 'w': 394}, 392: {'n': 408, 'e': 281}, 408: {'n': 443, 's': 392}, 443: {'s': 408, 'w': 477}, 481: {'n': 472, 'w': 485}, 472: {'n': 466, 's': 481, 'e': 495}, 466: {'n': 378, 's': 472}, 378: {'s': 466, 'w': 335}, 280: {'n': 234}, 234: {'n': 133, 's': 280, 'e': 259, 'w': 247}, 133: {'s': 234, 'e': 118, 'w': 151}, 157: {'e': 110}, 153: {'e': 97}, 113: {'e': 94, 'w': 145}, 68: {'e': 57}, 58: {'e': 23}, 80: {'n': 11, 'w': 83}, 11: {'s': 80, 'e': 3}, 36: {'e': 21, 'w': 41}, 19: {'n': 32, 'e': 15, 'w': 40}, 32: {'s': 19}, 79: {'e': 46, 'w': 106}, 63: {'n': 140, 'e': 61}, 140: {'s': 63}, 185: {'n': 195, 'e': 155, 'w': 292}, 195: {'s': 185}, 328: {'e': 200}, 199: {'n': 281, 'e': 197, 'w': 318}, 281: {'n': 350, 's': 199, 'w': 392}, 350: {'n': 425, 's': 281}, 425: {'n': 434, 's': 350}, 434: {'s': 425}, 495: {'w': 472}, 415: {'n': 306}, 306: {'n': 291, 's': 415}, 291: {'n': 259, 's': 306}, 259: {'s': 291, 'w': 234}, 118: {'n': 110, 'e': 218, 'w': 133}, 110: {'n': 97, 's': 118, 'w': 157}, 97: {'n': 94, 's': 110, 'w': 153}, 94: {'n': 57, 's': 97, 'w': 113}, 57: {'n': 23, 's': 94, 'w': 68}, 23: {'s': 57, 'e': 6, 'w': 58}, 16: {'e': 8}, 3: {'n': 21, 'e': 0, 'w': 11}, 21: {'s': 3, 'w': 36}, 15: {'e': 13, 'w': 19}, 47: {'e': 14}, 46: {'n': 61, 'e': 17, 'w': 79}, 61: {'n': 82, 's': 46, 'w': 63}, 82: {'n': 155, 's': 61}, 155: {'s': 82, 'w': 185}, 175: {'n': 200, 'e': 141}, 200: {'s': 175, 'e': 204, 'w': 328}, 197: {'e': 165, 'w': 199}, 223: {'n': 483, 'e': 169}, 483: {'s': 223}, 488: {'n': 409}, 409: {'n': 345, 's': 488}, 345: {'n': 261, 's': 409}, 261: {'n': 252, 's': 345}, 252: {'n': 218, 's': 261}, 218: {'n': 144, 's': 252, 'w': 118}, 144: {'n': 134, 's': 218}, 134: {'n': 65, 's': 144}, 65: {'n': 62, 's': 134}, 62: {'n': 6, 's': 65}, 6: {'s': 62, 'e': 5, 'w': 23}, 8: {'n': 0, 'w': 16}, 0: {'n': 4, 's': 8, 'e': 1, 'w': 3}, 4: {'s': 0}, 13: {'n': 14, 'e': 9, 'w': 15}, 14: {'n': 17, 's': 13, 'w': 47}, 17: {'n': 33, 's': 14, 'e': 28, 'w': 46}, 33: {'s': 17}, 102: {'n': 107, 'e': 64}, 107: {'n': 141, 's': 102}, 141: {'s': 107, 'w': 175}, 204: {'w': 200}, 165: {'n': 169, 'e': 163, 'w': 197}, 169: {'n': 385, 's': 165, 'w': 223}, 385: {'s': 169}, 497: {'e': 366}, 424: {'n': 322}, 322: {'s': 424, 'e': 276}, 290: {'n': 264}, 264: {'n': 244, 's': 290}, 244: {'s': 264, 'e': 232}, 181: {'n': 179}, 179: {'n': 96, 's': 181, 'e': 201}, 96: {'n': 66, 's': 179}, 66: {'n': 50, 's': 96}, 50: {'n': 5, 's': 66, 'e': 70}, 5: {'n': 2, 's': 50, 'w': 6}, 2: {'n': 1, 's': 5, 'e': 10}, 1: {'n': 7, 's': 2, 'e': 22, 'w': 0}, 7: {'n': 9, 's': 1, 'e': 12}, 9: {'s': 7, 'w': 13}, 30: {'n': 28}, 28: {'n': 60, 's': 30, 'w': 17}, 60: {'n': 64, 's': 28}, 64: {'n': 111, 's': 60, 'w': 102}, 111: {'n': 121, 's': 64, 'e': 114}, 121: {'n': 148, 's': 111, 'e': 123}, 148: {'n': 163, 's': 121, 'e': 178}, 163: {'n': 257, 's': 148, 'e': 228, 'w': 165}, 257: {'n': 388, 's': 163}, 388: {'s': 257, 'n': 386}, 386: {'e': 354, 's': 388}, 366: {'e': 361, 'w': 497}, 467: {'n': 459}, 459: {'n': 276, 's': 467}, 276: {'n': 268, 's': 459, 'w': 322}, 268: {'n': 265, 's': 276}, 265: {'n': 232, 's': 268, 'e': 273}, 232: {'n': 206, 's': 265, 'w': 244}, 206: {'n': 201, 's': 232}, 201: {'s': 206, 'w': 179}, 159: {'n': 116}, 116: {'n': 70, 's': 159}, 70: {'s': 116, 'e': 87, 'w': 50}, 38: {'n': 10}, 10: {'s': 38, 'w': 2}, 22: {'w': 1}, 12: {'n': 20, 'e': 18, 'w': 7}, 20: {'n': 31, 's': 12, 'e': 26}, 31: {'n': 37, 's': 20}, 37: {'n': 91, 's': 31, 'e': 42}, 91: {'n': 101, 's': 37}, 101: {'s': 91}, 114: {'e': 120, 'w': 111}, 123: {'e': 138, 'w': 121}, 178: {'w': 148}, 228: {'n': 253, 'w': 163}, 253: {'n': 285, 's': 228}, 285: {'s': 253}, 354: {'n': 361, 'e': 321, 'w': 386}, 361: {'s': 354, 'w': 366}, 455: {'n': 382}, 382: {'n': 296, 's': 455}, 296: {'n': 273, 's': 382, 'e': 308}, 273: {'s': 296, 'e': 298, 'w': 265}, 237: {'n': 229, 'e': 370}, 229: {'n': 212, 's': 237}, 212: {'n': 127, 's': 229}, 127: {'n': 117, 's': 212, 'e': 173}, 117: {'n': 87, 's': 127, 'e': 170}, 87: {'s': 117, 'w': 70}, 54: {'n': 29}, 29: {'n': 24, 's': 54}, 24: {'n': 18, 's': 29, 'e': 25}, 18: {'s': 24, 'e': 34, 'w': 12}, 26: {'n': 27, 'w': 20}, 27: {'s': 26, 'e': 55}, 42: {'n': 51, 'w': 37}, 51: {'n': 93, 's': 42}, 93: {'s': 51}, 120: {'w': 114}, 138: {'n': 143, 'e': 139, 'w': 123}, 143: {'s': 138}, 233: {'n': 240, 'e': 152}, 240: {'n': 304, 's': 233}, 304: {'n': 321, 's': 240}, 321: {'n': 334, 's': 304, 'w': 354}, 334: {'s': 321, 'e': 384}, 416: {'n': 317}, 317: {'n': 308, 's': 416}, 308: {'s': 317, 'e': 337, 'w': 296}, 298: {'e': 360, 'w': 273}, 370: {'w': 237}, 267: {'n': 202, 'e': 302}, 202: {'n': 173, 's': 267, 'e': 249}, 173: {'s': 202, 'w': 127}, 170: {'n': 182, 'w': 117}, 182: {'s': 170, 'e': 211}, 77: {'n': 43, 'e': 130}, 43: {'n': 25, 's': 77, 'e': 49}, 25: {'s': 43, 'w': 24}, 34: {'n': 35, 'e': 39, 'w': 18}, 35: {'s': 34, 'e': 44}, 55: {'n': 56, 'w': 27}, 56: {'n': 73, 's': 55, 'e': 67}, 73: {'n': 132, 's': 56}, 132: {'n': 172, 's': 73}, 172: {'s': 132}, 139: {'n': 147, 'e': 176, 'w': 138}, 147: {'n': 152, 's': 139, 'e': 154}, 152: {'n': 196, 's': 147, 'w': 233}, 196: {'n': 278, 's': 152, 'e': 224}, 278: {'n': 338, 's': 196}, 338: {'s': 278}, 384: {'e': 435, 'w': 334}, 460: {'n': 383}, 383: {'n': 337, 's': 460}, 337: {'s': 383, 'w': 308}, 360: {'n': 364, 'w': 298}, 364: {'s': 360, 'e': 401}, 302: {'e': 402, 'w': 267}, 249: {'w': 202}, 272: {'n': 248}, 248: {'n': 211, 's': 272}, 211: {'s': 248, 'w': 182}, 130: {'w': 77}, 49: {'e': 119, 'w': 43}, 52: {'n': 39}, 39: {'s': 52, 'e': 71, 'w': 34}, 44: {'n': 48, 'e': 59, 'w': 35}, 48: {'s': 44, 'e': 53}, 67: {'n': 84, 'w': 56}, 84: {'n': 86, 's': 67}, 86: {'n': 146, 's': 84, 'e': 95}, 146: {'s': 86}, 176: {'w': 139}, 154: {'n': 192, 'e': 184, 'w': 147}, 192: {'s': 154, 'e': 239}, 224: {'n': 287, 'w': 196}, 287: {'n': 313, 's': 224, 'e': 353}, 313: {'s': 287}, 435: {'w': 384}, 464: {'n': 420}, 420: {'n': 401, 's': 464}, 401: {'s': 420, 'e': 427, 'w': 364}, 402: {'e': 403, 'w': 302}, 371: {'n': 309, 'e': 430}, 309: {'n': 286, 's': 371, 'e': 377}, 286: {'n': 242, 's': 309, 'e': 288}, 242: {'n': 219, 's': 286}, 219: {'n': 119, 's': 242, 'e': 305}, 119: {'s': 219, 'e': 131, 'w': 49}, 115: {'n': 71, 'e': 160}, 71: {'s': 115, 'e': 150, 'w': 39}, 59: {'e': 189, 'w': 44}, 53: {'n': 75, 'w': 48}, 75: {'n': 78, 's': 53, 'e': 88}, 78: {'s': 75, 'e': 90}, 95: {'n': 109, 'w': 86}, 109: {'n': 136, 's': 95}, 136: {'s': 109, 'e': 231}, 184: {'w': 154}, 239: {'n': 255, 'e': 336, 'w': 192}, 255: {'s': 239}, 353: {'n': 380, 'w': 287}, 380: {'n': 476, 's': 353, 'e': 445}, 476: {'s': 380}, 496: {'n': 475}, 475: {'n': 448, 's': 496}, 448: {'n': 438, 's': 475, 'e': 490}, 438: {'n': 427, 's': 448}, 427: {'s': 438, 'e': 474, 'w': 401}, 403: {'e': 439, 'w': 402}, 430: {'e': 440, 'w': 371}, 377: {'e': 456, 'w': 309}, 288: {'n': 326, 'e': 498, 'w': 286}, 326: {'s': 288}, 305: {'e': 330, 'w': 219}, 131: {'e': 329, 'w': 119}, 160: {'e': 214, 'w': 115}, 150: {'e': 251, 'w': 71}, 189: {'e': 275, 'w': 59}, 103: {'n': 88}, 88: {'s': 103, 'e': 125, 'w': 75}, 90: {'n': 98, 'e': 142, 'w': 78}, 98: {'n': 186, 's': 90}, 186: {'s': 98, 'e': 262}, 231: {'n': 282, 'e': 294, 'w': 136}, 282: {'s': 231}, 336: {'n': 373, 'e': 421, 'w': 239}, 373: {'s': 336}, 480: {'n': 445}, 445: {'s': 480, 'e': 446, 'w': 380}, 490: {'w': 448}, 474: {'w': 427}, 439: {'w': 403}, 440: {'w': 430}, 456: {'w': 377}, 498: {'w': 288}, 348: {'n': 330}, 330: {'s': 348, 'e': 454, 'w': 305}, 329: {'e': 407, 'w': 131}, 214: {'e': 246, 'w': 160}, 251: {'w': 150}, 275: {'e': 283, 'w': 189}, 198: {'n': 125, 'e': 270}, 125: {'s': 198, 'e': 238, 'w': 88}, 142: {'n': 245, 'w': 90}, 245: {'s': 142, 'e': 343}, 262: {'e': 390, 'w': 186}, 294: {'n': 363, 'e': 311, 'w': 231}, 363: {'s': 294}, 421: {'w': 336}, 446: {'w': 445}, 454: {'w': 330}, 407: {'w': 329}, 246: {'n': 325, 'e': 412, 'w': 214}, 325: {'s': 246}, 283: {'e': 376, 'w': 275}, 270: {'e': 300, 'w': 198}, 238: {'n': 381, 'e': 293, 'w': 125}, 381: {'s': 238, 'e': 431}, 343: {'w': 245}, 390: {'e': 398, 'w': 262}, 311: {'n': 389, 'e': 499, 'w': 294}, 389: {'s': 311}, 412: {'w': 246}, 468: {'n': 376}, 376: {'s': 468, 'w': 283}, 300: {'e': 320, 'w': 270}, 293: {'w': 238}, 431: {'w': 381}, 487: {'n': 398}, 398: {'s': 487, 'w': 390}, 499: {'w': 311}, 471: {'n': 320}, 320: {'s': 471, 'w': 300}}

# BFS Test
dd = Graph()  # Instantiate 
dd.add_vertex_number(500)
for key, value in edges_dict.items():
    for i in value:
        #print(key, i)
        dd.add_one_edge(key, i)
print("test check 500 is ", len(edges_dict))
print("test check 500 is ", len(my_map2))
print("alt BFS test", dd.bfs(1, 4))

# Steps:
# 1. walk in one direction until you hit a dead end (or find a room you found already)
# as you walk, record (somewhere) where options to go a different direction are (intersections)
# 2. if you are at a dead end, go to the nearest cross-roads and go in a new direction.
# 3. record the directions you walked in, as your traversal path.




#####
## Goal: output a compelete traversal_path list
#####

# for testing (just 10 turns)
#for i in range(15):

# for testing (small map)
#while len(rooms_visited_set) < 18:


# keep walking until you visit every room:
#while rooms_visited_set != set_of_all_room_numbers:

# for testing (just X turns)
# for i in range(2000):

# keep walking until you visit every room:
# while rooms_visited_set != set_of_all_room_numbers:

# keep walking until you visit every room:
# while rooms_visited_set != set_of_all_room_numbers:

# for testing (just X turns)
#while 6 not in crossroads_set:

# for testing (just X turns)
for i in range(500):

    # inspection
    print(f"\n Taking Another Step (step: {step_counter})...!!! Now in room {player.current_room.id}.")
    print("# of rooms visited:", len(rooms_visited_set))
    print("map so far...", my_map)
    # print("rooms_visited_set so far...", rooms_visited_set)
    print("crossroads_set so far...", crossroads_set)
    # print("Path so far...", traversal_path)
    print("\n")

    ## plan for moving:
    # first if-else: either you can keep going 'forward' 
    # 
    # there are 3 options if you cannot go in the same direction
    # 1. go right
    # 2. go left
    # 3. go back to lass crossroads

    ## continue in same direction, unless not an option:
    ## note: a dead end is where you can only go back, 
    ## so try right and left before going to last crossroads.
    ## No other options but 'go back,' go back to  
    ## the nearest explored crossroads

    # check for dead-end
    # check if you have to 'to back' to the last unexplored crossroads path:
    if this_direction not in player.current_room.get_exits() and try_going_right[this_direction] not in player.current_room.get_exits() and try_going_left[this_direction] not in player.current_room.get_exits():

        # dead end is where you can only go back, try right and left before going to last crossroads.
        # if you can't go right or left: go back to last unexplored crossroads:

        #### Plans
        ## Since you hit a dead end, find the closest path back to the nearest
        ## unexplored crossroads:
        ## check distance to each room on your crossraods list
        ## which rooms contain unexplored crossroads?
        ## check map-room-dictionaries for question-marks

        # find last crossroads
        print(f"\n Hit a dead end. Now in room {player.current_room.id}.")        
        # start with a blank navidation dict:
        # this will be filled with {distance : room} results
        navigation_dict = {}

        # # print inspection
        #print("crossroads_set1", crossroads_set)
        #print("rooms_visited_set1", rooms_visited_set)        
        print("Cross_roads search Print set:")
        # print("rooms_visited_set1", rooms_visited_set)
        # print("full path", dungeon_graph.bfs_all_path(current_room, this_room_id))
        # print("bfs old path", dungeon_graph.bfs(current_room, this_room_id))

        # Step: find next-closest-crossroads
        # check which room in the crossroads_set is closest: 
        # keep track of the distances using the navigation_dictionary
        # {lenth of path : which room that is to}

        # make an updated dictionary of distances to crossroads
        # relative to where you are:
        for this_room_id in crossroads_set:
            # using mask for readability
            # remove current room from path to next room
            room_distance_mask = len(dungeon_graph.bfs_all_path(player.current_room.id, this_room_id)[1:])
            # # Alt For Testing
            room_distance_mask_alt = len(dd.bfs(player.current_room.id, this_room_id)[1:])
            # make entry in navigation_dict
            # {lenth of path : which room that is to}
            navigation_dict[room_distance_mask] = this_room_id

            # # inspection
            # print("room_distance_mask_alt", room_distance_mask_alt)
            # print("room_distance_mask", room_distance_mask)
            # print("full path", dungeon_graph.bfs_all_path(current_room, this_room_id))
            # print("room_distance_mask_alt", room_distance_mask_alt)
            # print("current_room", current_room)
            # print("player.current_room.id", player.current_room.id)


        # pick the shortest distance in that list of crossroads distances
        mask_min_distance = min(list(navigation_dict.keys()))
        crossroads_room_I_want = navigation_dict[mask_min_distance]

        # Find the direction you want
        # The direction you want is:
        # the direction (n,w,e,s) to 
        # the smallest (min) number 
        # in list of keys (distances) in your distance dictionary
        # hence: crossroads_room_I_want = the closest such room

        # inspection 
        print("crossroads_room_I_want:", crossroads_room_I_want)
        print("I am here now:", player.current_room.id)
        print("BFS path 1", dungeon_graph.bfs_all_path(player.current_room.id, crossroads_room_I_want))
        print("BFS path 2", dd.bfs(player.current_room.id, crossroads_room_I_want))
        
        # step: quickmarch
        # quickmarch all the steps to that crossroads
        # follow each step in traversal list, and add that step
        # to your traversal_path
        # each pass though this while loop takes one step closer
        # note: this might take you down a new path...maybe?
        while player.current_room.id != crossroads_room_I_want:
            # # inspection
            print(" \n Quickmarching, current room is:", player.current_room.id)
            print("crossroads_room_I_want", crossroads_room_I_want)
            print("path", dungeon_graph.bfs_all_path(current_room, crossroads_room_I_want))

            # get id of the next_room_along_the_way
            # note: the 'first' [0] room is the current room
            # so you want the 2nd room [1]
            next_room_along_the_way = dungeon_graph.bfs_all_path(player.current_room.id, crossroads_room_I_want)[1]
            next_room_along_the_way_alt = dd.bfs(player.current_room.id, crossroads_room_I_want)[1]

            # get directions to go to that room from current_room
            # make a mask:
            here = my_map[player.current_room.id]
            # Alt for testing
            # here = my_map2[player.current_room.id]

            # reverse (value -> key) lookup of which direction the next room is in:
            this_direction = list(here.keys())[list(here.values()).index(next_room_along_the_way)]

            # # inspection
            print("moving to new room")
            print("you are here:")
            print("current_room", current_room)
            print("player.current_room.id", player.current_room.id)
            print("\n Moving in this direction:")
            print("this_direction", this_direction)
            # print("nodes", dungeon_graph.vertices)
            # print("my_map", my_map)
            # print("compare, map2", my_map2)
            print("mask for 'here'", here)

            print("next_room_along_the_way", next_room_along_the_way)
            print("next_room_along_the_way_alt", next_room_along_the_way_alt)
            print("step_counter", step_counter)

            # # Move and update rooms
            # for setting previous room
            current_room = player.current_room.id
            # # go in that direction
            player.travel(this_direction)
            # where you were
            previous_room = current_room
            # where you are
            current_room = player.current_room.id

            #####
            ## New Room
            #####

            # if this is a new room
            if player.current_room.id not in rooms_visited_set:

                # add to your map (add your current location)
                make_map(player.current_room.id)

                # add new room to the graph
                dungeon_graph.add_dungeon_vertex(player.current_room.id)

                # update edges on maps:
                # print(current_room, previous_room)
                dungeon_graph.add_edge_bidirectional(player.current_room.id, previous_room)

                # # Step: update '?' in map for cross-roads
                # e.g. each time you go to a new room:
                # 1. the last room should be updated to include the new room
                my_map[previous_room][this_direction] = player.current_room.id

                # 2. the new room should be updated to include the old room   
                # use reverse direction to update 
                # the current room "backwards" to the last room
                my_map[player.current_room.id][reverse_direction_dict[this_direction]] = previous_room

                # updated rooms_visited_set
                rooms_visited_set.add(player.current_room.id)

                # Step: update the crossroads set
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

            ## Updates for all moves:

            # Record your traversal path
            # Even if you have been there before!!
            traversal_path.extend([this_direction])
            step_counter += 1

            ### end of "dead end" fork

        # Then, at the crossroads: pick a new direction
        direction_to_try = random.choice(player.current_room.get_exits())
        # check to see if that new door has not yet been opened (must be '?' on my_map)
        while my_map[player.current_room.id][direction_to_try] != '?':
            direction_to_try = random.choice(player.current_room.get_exits())
        # update 'this direction' 
        this_direction = direction_to_try

        # print inspection
        print("\n Picking a crossroads: let's go", this_direction)

    # so, not dead end:
    else: # if you can keep going (stright, left or right)
        
        ## if you can, keep going straight (nothing to change in that case)
        if this_direction in player.current_room.get_exits():
            pass

        # otherwise, if either right or left is an option...
        elif try_going_right[this_direction] in player.current_room.get_exits() or try_going_left[this_direction] in player.current_room.get_exits():
            # if not left, go right:
            if try_going_left[this_direction] not in player.current_room.get_exits():
                this_direction = try_going_right[this_direction]

                # inspection
                print("change to", this_direction)

            else:  # otherwise: go left
                this_direction = try_going_left[this_direction]

                # inspection
                print("change to", this_direction)

        # # Move and update rooms
        # for setting previous room
        current_room = player.current_room.id
        # # go in that direction
        player.travel(this_direction)
        # where you were
        previous_room = current_room
        # where you are
        current_room = player.current_room.id

        #####
        ## New Room
        #####

        # if this is a new room
        if player.current_room.id not in rooms_visited_set:

            # add to your map (add your current location)
            make_map(player.current_room.id)

            # add new room to the graph
            dungeon_graph.add_dungeon_vertex(player.current_room.id)

            # update edges on maps:
            # print(current_room, previous_room)
            dungeon_graph.add_edge_bidirectional(player.current_room.id, previous_room)

            # # Step: update '?' in map for cross-roads
            # e.g. each time you go to a new room:
            # 1. the last room should be updated to include the new room
            my_map[previous_room][this_direction] = player.current_room.id

            # 2. the new room should be updated to include the old room   
            # use reverse direction to update 
            # the current room "backwards" to the last room
            my_map[player.current_room.id][reverse_direction_dict[this_direction]] = previous_room

            # updated rooms_visited_set
            rooms_visited_set.add(player.current_room.id)

            # Step: update the crossroads set
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

        ## Updates for all moves:
        # Record your traversal path
        # Even if you have been there before!!
        traversal_path.extend([this_direction])
        step_counter += 1

        ### end of "not dead end" fork

    # Inspection
    print("data from end of move: \n")
    # print("this room", player.current_room.id)
    # print("traversal_path", traversal_path)
    # print("my map", my_map)
    print("this_direction", this_direction)
    # print("rooms_visited_set", rooms_visited_set)
    # print("crossroads_set", crossroads_set)
    # print("path:", traversal_path)
    # print("nodes", dungeon_graph.vertices)
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
