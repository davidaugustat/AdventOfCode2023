def map_value(value, mapping):
    for (dst_range, src_range, l) in mapping:
        if value >= src_range and value < src_range + l:
            return dst_range + (value - src_range)
    return value
        

def map_value_reverse(value, mapping):
    for (dst_range, src_range, l) in mapping:
        if value >= dst_range and value < dst_range + l:
            return src_range + (value - dst_range)
    return value


def numbers_string_to_int_array(text):
    return [int(s) for s in text.split()]


def parse_map(text):
    map_tuples = []
    lines = text.split(':')[1].strip().split('\n')
    for line in lines:
        map_tuples.append(numbers_string_to_int_array(line))
    return map_tuples


def seed_to_location(seed, maps):
    value = seed
    for map in maps:
        value = map_value(value, map)
    return value


def location_to_seed(location, maps_reversed):
    value = location
    for map in maps_reversed:
        value = map_value_reverse(value, map)
    return value


def find_lowest_location(seeds, maps):
    locations = [seed_to_location(seed, maps) for seed in seeds]
    print(locations)
    return min(locations)


def is_seed_in_range(seed_to_check, seeds):
    for i in range(0, len(seeds), 2):
        if seed_to_check >= seeds[i] and seed_to_check < seeds[i] + seeds[i+1]:
            return True
    return False


def find_lowest_location_part2(seeds, maps):
    maps_reverse = maps[::-1]
    location = 0
    while True:
        seed = location_to_seed(location, maps_reverse)
        if is_seed_in_range(seed, seeds):
            print(f"Seed: {seed}")
            return location
        location += 1

        
def read_data_from_file(filename):
    with open(filename) as file:
        content = file.read()
        sections = content.split('\n\n')

        seeds = numbers_string_to_int_array(sections[0].split(':')[1])
        print(seeds)

        maps = [parse_map(section) for section in sections[1:]]
        print(maps)
        return seeds, maps


# seeds, maps = read_data_from_file("testinput.txt")
seeds, maps = read_data_from_file("input.txt")

# print(seed_to_location(2087136879, maps))
# print(find_lowest_location(seeds, maps))
print(find_lowest_location_part2(seeds, maps))
