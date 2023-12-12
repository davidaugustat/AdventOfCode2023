from functools import lru_cache


def get_length_until_next_dot(sequence):
    i=0
    while i < len(sequence) and sequence[i] != '.':
        i += 1
    return i


@lru_cache(maxsize=None) # Cache to speed up recursion
def get_num_options(sequence, nums):
    if len(sequence) == 0:
        return 0 if len(nums) > 0 else 1
    
    if len(nums) == 0:
        return 0 if '#' in sequence else 1
    
    if sequence[0] == '.':
        return get_num_options(sequence[1:], nums)
    
    num_options = 0
    if sequence[0] in ['#', '?']:
        # option 1: Place block here
        if get_length_until_next_dot(sequence) >= nums[0]:
            if len(sequence) == nums[0]:
                return 1 if len(nums) == 1 else 0

            if sequence[nums[0]] != '#':
                num_options += get_num_options(sequence[nums[0]+1:], nums[1:])
    
    if sequence[0] == '?':
        # option 2: Don't place block here
        num_options += get_num_options(sequence[1:], nums)
    
    return num_options


def get_sum_of_option_counts(data):
    return sum([get_num_options(sequence, nums) for sequence, nums in data])


def unfold_data(data):
    unfolded_data = []
    for sequence, nums in data:
        new_sequence = '?'.join([sequence]*5)
        new_nums = nums * 5
        unfolded_data.append((new_sequence, new_nums))
    return unfolded_data


def read_data_from_file(filename):
    data = []
    with open(filename) as file:
        for line in file:
            sequence, num_string = line.rstrip().split()
            numbers = tuple([int(num) for num in num_string.split(',')])
            data.append((sequence, numbers))
    return data


data = read_data_from_file("input.txt")
# data = read_data_from_file("testinput.txt")
unfolded_data = unfold_data(data)

part1_result = get_sum_of_option_counts(data)
print("Part 1 result:", part1_result)

part2_result = get_sum_of_option_counts(unfolded_data)
print("Part 2 result:", part2_result)
