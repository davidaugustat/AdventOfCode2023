from tqdm import tqdm
from copy import deepcopy
import math

def tilt_platform(platform, dir):
    r = len(platform)
    c = len(platform[0])

    if dir == "north":
        diff_x = 0
        diff_y = -1
    elif dir == "south":
        diff_x = 0
        diff_y = 1
    elif dir == "west":
        diff_x = -1
        diff_y = 0
    elif dir == "east":
        diff_x = 1
        diff_y = 0
    else:
        raise Exception("Invalid direction")
    
    change = True
    while change:
        change = False
        for i in range(r):
            for j in range(c):
                tar_x, tar_y = j + diff_x, i + diff_y
                if platform[i][j] == 'O' and tar_x >= 0 and tar_x < c and tar_y >= 0 and tar_y < r and platform[tar_y][tar_x] == '.':
                    platform[i][j] = '.'
                    platform[tar_y][tar_x] = 'O'
                    change = True
    return platform


def calc_weight(platform):
    r = len(platform)
    c = len(platform[0])

    weight = 0
    for i in range(r):
        for j in range(c):
            if platform[i][j] == 'O':
                weight += r - i
    return weight


def part1(platform):
    tilt_platform(platform, "north")
    weight = calc_weight(platform)
    print("Part 1 Weight:", weight)


def find_cycle(platform):
    history = [deepcopy(platform)]
    weights_history = []
    for cycle in tqdm(range(1_000_000_000)):
        tilt_platform(platform, "north")
        tilt_platform(platform, "west")
        tilt_platform(platform, "south")
        tilt_platform(platform, "east")
        weight = calc_weight(platform)

        if weight in weights_history and platform in history:
            first_occ = history.index(platform)
            second_occ = cycle
            cycle_length = second_occ - first_occ + 1
            return cycle_length, first_occ, weights_history
        
        history.append(deepcopy(platform))
        weights_history.append(weight)

        
def get_weight_at_iteration(iteration, cycle_length, cycle_start, weights_history):
    pos_in_cycle = iteration % cycle_length
    # Make sure that position is after cycle_start:
    pos = pos_in_cycle + cycle_length * math.ceil((cycle_start-pos_in_cycle)/cycle_length) - 1
    return weights_history[pos]


def part2(platform):
    cycle_length, cycle_start, weights_history = find_cycle(platform)
    result = get_weight_at_iteration(1_000_000_000, cycle_length, cycle_start, weights_history)
    print("Part 2 weight:", result)


def read_data_from_file(filename):
    with open(filename) as file:
        platform = [[c for c in line.rstrip()] for line in file]
        return platform


platform = read_data_from_file("input.txt")
# platform = read_data_from_file("testinput.txt")

# part1(platform)
part2(platform)
