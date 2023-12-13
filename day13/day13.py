def rotate_pattern(pattern):
    res = list(zip(*pattern))
    return [''.join(r) for r in res]


def find_horizontal_reflection(pattern, forbidden_center=None):
    center_candidates = []
    # find consecutive pairs of equal rows:
    for i1 in range(len(pattern)):
        for i2 in range(i1+1, len(pattern)):
            if pattern[i1] == pattern[i2]:
                center_candidates.append(i2) # center is larger row of two center rows

    center_candidates = [e for e in center_candidates if e != forbidden_center]

    for center in center_candidates:
        valid = True
        for i in range(center):
            if center + (center - i - 1) < len(pattern) and pattern[i] != pattern[center + (center - i - 1)]:
                valid = False
                break
        if valid:
            return True, center
    return False, 0


def part1(patterns):
    sum = 0
    for pattern in patterns:
        succ_hor, len_hor = find_horizontal_reflection(pattern)
        if succ_hor:
            sum += 100 * len_hor
        succ_ver, len_ver = find_horizontal_reflection(rotate_pattern(pattern))
        if succ_ver:
            sum += len_ver

    print("Sum Part 1:", sum)


def part2(patterns):
    sum = 0
    for pattern in patterns:
        succ_hor_orig, center_hor_orig = find_horizontal_reflection(pattern)
        succ_ver_orig, center_ver_orig = find_horizontal_reflection(rotate_pattern(pattern))
        break_i = False

        for i in range(len(pattern)):
            if break_i:
                break
            for j in range(len(pattern[0])):
                pat2 = pattern.copy()
                replacement = '#' if pat2[i][j] == '.' else '.'
                pat2[i] = pat2[i][:j] + replacement + pat2[i][j+1:]

                succ_hor, center_hor = find_horizontal_reflection(pat2, center_hor_orig if succ_hor_orig else None)
                if succ_hor:
                    sum += 100 * center_hor
                    break_i = True
                    break
                succ_ver, center_ver = find_horizontal_reflection(rotate_pattern(pat2), center_ver_orig if succ_ver_orig else None)
                if succ_ver:
                    sum += center_ver
                    break_i = True
                    break

    print("Sum Part 2:", sum)


def print_pattern(pattern):
    for line in pattern:
        print(line)


def read_data_from_file(filename):
    patterns = []
    with open(filename) as file:
        current_pattern = []
        for line in file:
            if line == '\n' or line == '\r\n':
                patterns.append(current_pattern)
                current_pattern = []
            else:
                current_pattern.append(line.rstrip())
        patterns.append(current_pattern)
    return patterns


patterns = read_data_from_file("input.txt")
# patterns = read_data_from_file("testinput.txt")

part1(patterns)
part2(patterns)
