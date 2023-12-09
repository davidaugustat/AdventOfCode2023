def is_all_zeros(array):
    return all(v == 0 for v in array)


def find_differences(history):
    diffs = [history]
    while not is_all_zeros(diffs[-1]):
        previous = diffs[-1]
        diff = []
        for i in range(len(previous)-1):
            diff.append(previous[i+1] - previous[i])
        diffs.append(diff)
    return diffs


def extrapolate_last(diffs):
    extrapolated = [0]
    for i in range(len(diffs)-2, -1, -1):
        extrapolated.append(diffs[i][-1] + extrapolated[-1])
    return extrapolated[-1]


def extrapolate_first(diffs):
    extrapolated = [0]
    for i in range(len(diffs)-2, -1, -1):
        extrapolated.append(diffs[i][0] - extrapolated[-1])
    return extrapolated[-1]


def part1(histories):
    result = sum([extrapolate_last(find_differences(history)) for history in histories])
    print(f"Result part 1: {result}")


def part2(histories):
    result = sum([extrapolate_first(find_differences(history)) for history in histories])
    print(f"Result part 2: {result}")


def read_data_from_file(filename):
    histories = []
    with open(filename) as file:
        for line in file:
            line_string = line.rstrip()
            split = line_string.split()
            histories.append([int(value) for value in split])
    return histories


# histories = read_data_from_file("testinput.txt")
histories = read_data_from_file("input.txt")

part1(histories)
part2(histories)