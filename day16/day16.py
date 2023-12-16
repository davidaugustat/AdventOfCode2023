def get_next_directions(tile, current_direction):
    if tile == '.':
        return [current_direction]
    
    if tile == "/":
        if current_direction == "l":
            return ["d"]
        if current_direction == "r":
            return ["u"]
        if current_direction == "u":
            return ["r"]
        if current_direction == "d":
            return ["l"]
        
    if tile == "\\":
        if current_direction == "l":
            return ["u"]
        if current_direction == "r":
            return ["d"]
        if current_direction == "u":
            return ["l"]
        if current_direction == "d":
            return ["r"]
        
    if tile == "|":
        if current_direction in "ud":
            return [current_direction]
        return ["u", "d"]
    
    if tile == "-":
        if current_direction in "lr":
            return [current_direction]
        return ["l", "r"]
    
    raise Exception("Invalid tile!")


def get_next_tile(i, j, dir, grid):
    if dir == "l":
        i_next, j_next = i, j-1
    if dir == "r":
        i_next, j_next = i, j+1
    if dir == "u":
        i_next, j_next = i-1, j
    if dir == "d":
        i_next, j_next = i+1, j
    
    if i_next < 0 or i_next >= len(grid) or j_next < 0 or j_next >= len(grid[0]):
        return None, None
    return i_next, j_next


def trace_light(grid, start_i, start_j, start_dir):
    r = len(grid)
    c = len(grid[0])

    energized_count = 0
    energized = [[False for _ in range(c)] for _ in range(r)]
    dirs_applied_to_tile = [[[] for _ in range(c)] for _ in range(r)]

    to_process = [(start_i, start_j, start_dir)]
    while len(to_process) > 0:
        i, j, dir = to_process.pop()
        if not energized[i][j]:
            energized[i][j] = True
            energized_count += 1
        if dir not in dirs_applied_to_tile[i][j]:
            dirs_applied_to_tile[i][j].append(dir)

        next_dirs = get_next_directions(grid[i][j], dir)
        for next_dir in next_dirs:
            i_next, j_next = get_next_tile(i, j, next_dir, grid)
            if i_next != None and next_dir not in dirs_applied_to_tile[i_next][j_next]:
                to_process.append((i_next, j_next, next_dir))
    
    return energized_count


def part1(grid):
    energized_count = trace_light(grid, 0, 0, "r")
    print("Part 1 Result:", energized_count)


def part2(grid):
    r = len(grid)
    c = len(grid[0])

    max_top_row = max(trace_light(grid, 0, j, "d") for j in range(c))
    max_bottom_row = max(trace_light(grid, r-1, j, "u") for j in range(c))
    max_left_row = max(trace_light(grid, i, 0, "r") for i in range(r))
    max_right_row = max(trace_light(grid, i, c-1, "l") for i in range(r))

    max_energized = max(max_top_row, max_bottom_row, max_left_row, max_right_row)
    print("Part 2 Result:", max_energized)
     

def read_data_from_file(filename):
    with open(filename) as file:
        grid = [line.rstrip() for line in file]
        return grid


grid = read_data_from_file("input.txt")
# grid = read_data_from_file("testinput.txt")

part1(grid)
part2(grid)
