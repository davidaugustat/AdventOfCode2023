import dijkstar.algorithm, dijkstar.graph

dirs = ["l", "r", "u", "d"]


def check_bounds(i, j, r, c):
    return i >= 0 and i < r and j >= 0 and j < c


def get_successors_part1(node, r, c):
    i, j, prev_dir, steps_taken_in_this_dir = node
    successors = []

    for next_dir in dirs:
        if next_dir == "l":
            if prev_dir == "r":
                continue
            i_next, j_next  =i, j-1
        elif next_dir == "r":
            if prev_dir == "l":
                continue
            i_next, j_next  =i, j+1
        elif next_dir == "u":
            if prev_dir == "d":
                continue
            i_next, j_next  =i-1, j
        elif next_dir == "d":
            if prev_dir == "u":
                continue
            i_next, j_next  =i+1, j
        else:
            raise Exception("Invalid direction")
        
        if (prev_dir != next_dir or (prev_dir == next_dir and steps_taken_in_this_dir < 3)) and check_bounds(i_next, j_next, r, c):
            steps = 1 if prev_dir != next_dir else steps_taken_in_this_dir + 1
            successors.append((i_next, j_next, next_dir, steps))
    return successors


def get_successors_part2(node, r, c):
    i, j, prev_dir, steps_taken_in_this_dir = node
    successors = []

    for next_dir in dirs:
        if steps_taken_in_this_dir < 4 and next_dir != prev_dir:
            continue

        if next_dir == "l":
            if prev_dir == "r":
                continue
            i_next, j_next  =i, j-1
        elif next_dir == "r":
            if prev_dir == "l":
                continue
            i_next, j_next  =i, j+1
        elif next_dir == "u":
            if prev_dir == "d":
                continue
            i_next, j_next  =i-1, j
        elif next_dir == "d":
            if prev_dir == "u":
                continue
            i_next, j_next  =i+1, j
        else:
            raise Exception("Invalid direction")
        
        # Before reaching end node, direction must stay the same for 4 steps:
        if i_next == r-1 and j_next == c-1:
            if next_dir != prev_dir or steps_taken_in_this_dir < 3:
                continue
        
        if (prev_dir != next_dir or (prev_dir == next_dir and steps_taken_in_this_dir < 10)) and check_bounds(i_next, j_next, r, c):
            steps = 1 if prev_dir != next_dir else steps_taken_in_this_dir + 1
            successors.append((i_next, j_next, next_dir, steps))
    return successors


def build_graph(grid, max_steps_one_dir=3, get_successors=get_successors_part1):
    r = len(grid)
    c  = len(grid[0])

    g = dijkstar.Graph()
    for i in range(r):
        for j in range(c):
            if not (i == 0 and j == 0): # start node has no predecessor direction
                # node = (i, j, dir, steps_moved_with_this_dir)
                for dir in dirs:
                    for steps_taken_in_this_dir in range(1, max_steps_one_dir+1):
                        node = (i, j, dir, steps_taken_in_this_dir)
                        successors =  get_successors(node, r, c)
                        for successor in successors:
                            edge_weight = int(grid[successor[0]][successor[1]])
                            g.add_edge(node, successor, edge_weight)
    
    # Handle start node:
    start_node = (0, 0, "r", 0)
    right_of_start_node = (0, 1, "r", 1)
    below_start_node = (1, 0, "d", 1)
    g.add_edge(start_node, right_of_start_node, int(grid[0][1]))
    g.add_edge(start_node, below_start_node, int(grid[1][0]))

    return g


def find_shortest_distance(graph, max_steps_one_dir):
    r = len(grid)
    c  = len(grid[0])

    start_node = (0, 0, "r", 0)
    end_nodes = [(r-1, c-1, dir, steps) for dir in dirs for steps in range(1, max_steps_one_dir+1)]
    predecessors = dijkstar.algorithm.single_source_shortest_paths(graph, start_node)
    distances = []
    for end_node in end_nodes:
        try:
            distances.append(dijkstar.algorithm.extract_shortest_path_from_predecessor_list(predecessors, end_node).total_cost)
        except:
            pass # No edge with this end node exists in graph
    return min(distances)


def part1(grid):
    graph = build_graph(grid)
    min_distance = find_shortest_distance(graph, 3)
    print("Part 1 result:", min_distance)


def part2(grid):
    graph = build_graph(grid, 10, get_successors_part2)
    min_distance = find_shortest_distance(graph, 10)
    print("Part 2 result:", min_distance)


def read_data_from_file(filename):
    with open(filename) as file:
        grid = [line.rstrip() for line in file]
        return grid


# grid = read_data_from_file("testinput.txt")
# grid = read_data_from_file("testinput2.txt")
grid = read_data_from_file("input.txt")

part1(grid)
part2(grid)
