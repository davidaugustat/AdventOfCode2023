def find_empty_rows_and_columns(image):
    r = len(image)
    c = len(image[0])

    # find empty rows and columns:
    row_is_empty = [True for _ in range(r)]
    col_is_empty = [True for _ in range(c)]
    for i in range(r):
        for j in range(c):
            if image[i][j] != '.':
                row_is_empty[i] = False
                col_is_empty[j] = False
    
    empty_rows = [i for i in range(r) if row_is_empty[i]]
    empty_columns = [i for i in range(c) if col_is_empty[i]]
    return empty_rows, empty_columns


def expand_galaxies(galaxies, empty_rows, empty_cols, expansion_factor=1000000):
    # shift by row:
    for row in empty_rows[::-1]:
        for i in range(len(galaxies)):
            if galaxies[i][0] > row:
                galaxies[i] = (galaxies[i][0] + expansion_factor-1, galaxies[i][1])

    # shift by column:
    for col in empty_cols[::-1]:
        for i in range(len(galaxies)):
            if galaxies[i][1] > col:
                galaxies[i] = (galaxies[i][0], galaxies[i][1] + expansion_factor-1)

    return galaxies    


def find_galaxy_positions(image):
    galaxies = []
    r = len(image)
    c = len(image[0])
    for i in range(r):
        for j in range(c):
            if image[i][j] == '#':
                galaxies.append((i,j))
    return galaxies


def get_distance(galaxy1, galaxy2):
    return abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])


def find_distances_sum(galaxies):
    sum = 0
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            distance = get_distance(galaxies[i], galaxies[j])
            sum += distance
    return sum


def print_image(image):
    for r in image:
        print(''.join(r))


def expand_and_find_distance_sum(image, expansion_factor):
    galaxies = find_galaxy_positions(image)
    empty_rows, empty_cols = find_empty_rows_and_columns(image)
    expand_galaxies(galaxies, empty_rows, empty_cols, expansion_factor)
    return find_distances_sum(galaxies)


def read_data_from_file(filename):
    with open(filename) as file:
        image = [[c for c in line.rstrip()] for line in file]
        return image


image = read_data_from_file("input.txt")
# image = read_data_from_file("testinput.txt")

# part1_result = expand_and_find_distance_sum(image, 2)
# print("Part 1:", part1_result)

part2_result = expand_and_find_distance_sum(image, 1000000)
print("Part 2:", part2_result)
