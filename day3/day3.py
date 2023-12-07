symbols = ['!', '§', '$', '%', '&', '/', '{', '}', '(', ')', '[', ']', '=', '?', '*', '+', '~', '#', '-', '_', ',', ';', ':', '\\', '@', '^', '°']

def get_symbol_positions(schematic, symbols_list=symbols):
    positions = []

    r = len(schematic)
    c = len(schematic[0])
    for i in range(r):
        for j in range(c):
            if schematic[i][j] in symbols_list:
                positions.append((i,j))
    return positions


def get_number_positions(schematic):
    # Structure: (row, col, num_as_string)
    number_positions = []

    r = len(schematic)
    c = len(schematic[0])
    for i in range(r):
        j = 0
        while j < c:
            if schematic[i][j].isdigit():
                k = 1
                while(j+k < c and schematic[i][j+k].isdigit()):
                    k += 1
                num = schematic[i][j:j+k]
                number_positions.append((i, j, num))
                j += k-1
            j += 1
    return number_positions
            

def is_number_part_number(num_pos_info, schematic):
    i, j, num_string = num_pos_info
    r = len(schematic)
    c = len(schematic[0])

    for k in range(j, j + len(num_string)):
        potential_indices = [(i-1, k), (i+1, k), (i, k-1), (i, k+1), (i-1, k-1), (i-1, k+1), (i+1, k-1), (i+1, k+1)]
        for pot_i, pot_j in potential_indices:
            if pot_i < 0 or pot_i >= r or pot_j < 0 or pot_j >= c:
                continue
            if schematic[pot_i][pot_j] in symbols:
                return True
    return False


def is_number_adjacent_to(num_pos_info, star_i, star_j, schematic):
    i, j, num_string = num_pos_info
    r = len(schematic)
    c = len(schematic[0])

    for k in range(j, j + len(num_string)):
        potential_indices = [(i-1, k), (i+1, k), (i, k-1), (i, k+1), (i-1, k-1), (i-1, k+1), (i+1, k-1), (i+1, k+1)]
        for pot_i, pot_j in potential_indices:
            if pot_i < 0 or pot_i >= r or pot_j < 0 or pot_j >= c:
                continue
            if pot_i == star_i and pot_j == star_j:
                return True
    return False

def get_gear_ratios(schematic):
    gear_ratios = []
    star_positions = get_symbol_positions(schematic, ['*'])
    number_positions = get_number_positions(schematic)
    for star_i, star_j in star_positions:
        adjacent_numbers = []
        for num_pos in number_positions:
            if is_number_adjacent_to(num_pos, star_i, star_j, schematic):
                adjacent_numbers.append(int(num_pos[2]))
        if len(adjacent_numbers) == 2:
            gear_ratios.append(adjacent_numbers[0] * adjacent_numbers[1])
    return gear_ratios


def get_part_numbers(schematic):
    all_number_positions = get_number_positions(schematic)
    part_number_positions = filter(lambda num_pos : is_number_part_number(num_pos, schematic), all_number_positions)
    part_numbers = list(map(lambda part_number_pos : int(part_number_pos[2]), part_number_positions))
    return part_numbers


def read_data_from_file(filename):
    schematic = []
    with open(filename) as file:
        for line in file:
            line_string = line.rstrip()
            schematic.append(line_string)
    return schematic


schematic = read_data_from_file("input.txt")
# schematic = read_data_from_file("testinput.txt")

# print(schematic)
# print(schematic[0][3])

# symbol_positions = get_symbol_positions(schematic)
# print(symbol_positions)
# number_positions = get_number_positions(schematic)
# print(number_positions)

# print(is_number_part_number((0, 4, '224'), schematic))
# print(is_number_part_number((0, 12, '487'), schematic))
# print(is_number_part_number((1, 89, '439'), schematic))
# print(is_number_part_number((3, 118, '464'), schematic))

# part_numbers = get_part_numbers(schematic)
# print(part_numbers)
# print(f"Sum: {sum(part_numbers)}")

gear_ratios = get_gear_ratios(schematic)
print(gear_ratios)
print(f'Sum: {sum(gear_ratios)}')
