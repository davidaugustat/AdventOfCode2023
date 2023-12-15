def read_data_from_file(filename):
    with open(filename) as file:
        for line in file:
            strings = line.rstrip().split(',')
            return strings


def hash(string):
    result = 0
    for c in string:
        ascii_num = ord(c)
        result += ascii_num
        result *= 17
        result %= 256
    return result


def get_data_from_strings(strings):
    data = []
    for string in strings:
        if '=' in string:
            label, focal_length = string.split('=')
            data.append((label, '=', int(focal_length)))
        elif '-' in string:
            label = string[0:-1]
            data.append((label, '-'))
    return data
        

def process_boxes(lenses):
    boxes = [[] for _ in range(256)]
    for lense in lenses:
        box_num = hash(lense[0])
        labels_in_box = [lense[0] for lense in boxes[box_num]]
        if lense[1] == '-':
            if lense[0] in labels_in_box:
                index = labels_in_box.index(lense[0])
                del boxes[box_num][index]
        elif lense[1] == '=':
            if lense[0] in labels_in_box:
                index = labels_in_box.index(lense[0])
                boxes[box_num][index][1] = lense[2]
            else:
                boxes[box_num].append([lense[0], lense[2]])
    return boxes


def calc_focusing_power(boxes):
    result = 0
    for i, box in enumerate(boxes):
        for j, lense in enumerate(box):
            focusing_power_lens = (i+1) * (j+1) * lense[1]
            result += focusing_power_lens
    return result


def part1(strings):
    result = sum(hash(string) for string in strings)
    print("Part 1 Result:", result)


def part2(strings):
    data = get_data_from_strings(strings)
    boxes = process_boxes(data)
    focusing_power = calc_focusing_power(boxes)
    print("Part 2 Result:", focusing_power)

    
strings = read_data_from_file("input.txt")
# strings = read_data_from_file("testinput.txt")

part1(strings)
part2(strings)
