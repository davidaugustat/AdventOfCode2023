from tqdm import tqdm

def get_neighbors(garden, tile):
    r = len(garden)
    c = len(garden[0])
    i, j = tile
    potential_neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]

    def is_neighbor(node):
        i_pot, j_pot = node
        return i_pot >= 0 and i_pot < r and j_pot >= 0 and j_pot < c and garden[i_pot][j_pot] != '#'
    # return list(filter(i_pot >= 0 and i_pot < r and j_pot >= 0 and j_pot < c and garden[i][j] != '#' 
    #               for i_pot, j_pot in potential_neighbors))
    return list(filter(is_neighbor, potential_neighbors))
    

def reachable_tiles(garden, target_steps):
    r = len(garden)
    c = len(garden[0])
    start_tile = next((i,j) for j in range(c) for i in range(r) if garden[i][j] == 'S')
    current_tiles = {start_tile}
    for num_steps in tqdm(range(1, target_steps+1)):
        next_tiles = set()
        for tile in current_tiles:
            neighbors = get_neighbors(garden, tile)
            # print("Neighbors of", tile, ":", neighbors)
            next_tiles.update(neighbors)
        current_tiles = next_tiles
    print(current_tiles)
    return len(current_tiles)


def read_data_from_file(filename):
    with open(filename) as file:
        garden = [[c for c in line.rstrip()] for line in file]
        return garden

def part1(garden):
    result = reachable_tiles(garden, 64)
    print("Part 1 result:", result)


garden = read_data_from_file("input.txt")
# garden = read_data_from_file("testinput.txt")
# print(reachable_tiles(garden, 26501365))
part1(garden)
