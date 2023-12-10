import math
from tqdm import tqdm
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


"""
Notes on part 2:

The loop path forms a polygon. To find all tiles enclosed by the loop path, we
can check for each point that is not part of the loop, whether it is inside the
polygon formed by the loop:
https://en.wikipedia.org/wiki/Point_in_polygon

For this purpose, I use the shapely package.
Performing the point-in-polygon test for all points takes about 35 seconds on my
hardware.
"""

def is_connected(i1, j1, i2, j2, text_graph):
    r = len(text_graph)
    c  =len(text_graph[0])

    # Check invalid indices
    if i1 < 0 or j1 < 0 or i2 < 0 or j2 < 0 or i1 >= r or j1 >= c or i2 >= r or j2 >= c:
        return False
    
    # Check same node:
    if i1 == i2 and j1 == j2:
        return False
    
    t1 = text_graph[i1][j1]
    t2 = text_graph[i2][j2]
    
    # 2 left of 1:
    if i1 == i2 and j2 == j1 - 1:
        return t1 in ['-', 'J', '7', 'S'] and t2 in ['-', 'L', 'F', 'S']
    
     # 2 right of 1:
    if i1 == i2 and j2 == j1 + 1:
        return t1 in ['-', 'L', 'F', 'S'] and t2 in ['-', 'J', '7', 'S']
    
    # 2 above 1:
    if i2 == i1 - 1 and j1 == j2:
        return t1 in ['|', 'L', 'J', 'S'] and t2 in ['|', '7', 'F', 'S']
    
    # 2 below 1:
    if i2 == i1 + 1 and j1 == j2:
        return t1 in ['|', '7', 'F', 'S'] and t2 in ['|', 'L', 'J', 'S']
    
    return False


def get_connected_neighbors(i, j, text_graph):
    r = len(text_graph)
    c  =len(text_graph[0])

    potential_neighbors = [(i, j-1), (i, j+1), (i-1, j), (i+1, j)]
    neighbors = list(filter(lambda n : is_connected(i, j, n[0], n[1], text_graph), potential_neighbors))
    return neighbors


def build_graph(text_graph):
    r = len(text_graph)
    c  =len(text_graph[0])

    graph = [[[] for _ in range(c)] for _ in range(r)]
    for i in range(r):
        for j in range(c):
            graph[i][j] = get_connected_neighbors(i, j, text_graph)
    return graph


def follow_path(i, j, i_prev, j_prev, graph, text_graph):
    if text_graph[i][j] == 'S':
        raise Exception("Not supporting S as start node since multiple successors")
    
    if text_graph[i][j] == '.':
        return []

    path = [(i,j)]
    while True:
        neighbors = graph[i][j]
        if len(neighbors) < 2: # neighbors also include previous node, so 1 neighbor is not enough
            return path
        if text_graph[i][j] == 'S': # found the loop!
            return path
        
        successor = next(n for n in neighbors if n[0] != i_prev or n[1] != j_prev)
        i_prev, j_prev = i, j
        i, j = successor
        path.append((i,j))


def get_start_node(text_graph):
    for i, row in enumerate(text_graph):
        j = row.find('S')
        if j >= 0:
            return i, j
    raise Exception("No start node in graph!")


def find_paths_from_start(graph, text_graph, start_node):
    paths = []
    i_start, j_start = start_node
    print(f"Start node: ({i_start}, {j_start})")
    for i, j in graph[i_start][j_start]:
        path = follow_path(i, j, i_start, j_start, graph, text_graph)
        paths.append(path)
    return paths


def find_loop_path(graph, text_graph):
    start_node = get_start_node(text_graph)
    paths = find_paths_from_start(graph, text_graph, start_node)
    for path in paths:
        if path[-1] == start_node:
            distance = math.floor(len(path)/2)
            print("Distance:", distance)
            return path, distance
        

def part2(graph, text_graph):
    r = len(text_graph)
    c  =len(text_graph[0])

    path, _ = find_loop_path(graph, text_graph)
    polygon = Polygon(path)

    enclosed_tiles = []
    for i in tqdm(range(r)):
        for j in range(c):
            if (i,j) not in path and polygon.contains(Point(i,j)):
                enclosed_tiles.append((i,j))
    
    print("Enclosed tiles:", enclosed_tiles)
    print("Number of enclosed tiles:", len(enclosed_tiles))


def read_data_from_file(filename):
    with open(filename) as file:
        text_graph = [line.rstrip() for line in file]
        return text_graph


text_graph = read_data_from_file("input.txt")
# text_graph = read_data_from_file("testinput.txt")
# text_graph = read_data_from_file("testinput3.txt")
graph = build_graph(text_graph)

# find_loop_path(graph, text_graph)
part2(graph, text_graph)
