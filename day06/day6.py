# d = (45-h)*h
# d = (t_tot-h)*h
# = -h^2 + h*t_tot
# d: distance, h: Button holding time, t_tot: Total time

# Target:
# find all h with
# -h^2 + t_tot*h >= d
# -h^2 + t_tot*h -d >= 0
# 
# with 0 < h < d

import math

def num_integers_in_range(a,b):
    result = math.floor(b) - math.ceil(a) + 1
    if a.is_integer():
        result -= 1
    if b.is_integer():
        result -= 1
    return result

def get_zero_points(t_total, distance):
    # Parabola ax^2 + bx + c
    a = -1
    b = t_total
    c = -distance

    # ABC formula:
    sqrt_content = b**2 - 4*a*c
    if sqrt_content < 0:
        return []
    zero_0 = (-b + math.sqrt(b**2 - 4*a*c))/(2*a)
    zero_1 = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)

    if zero_0 == zero_1:
        return [zero_0]
    return [zero_0, zero_1] if zero_0 < zero_1 else [zero_1, zero_0]


def limit_to_bounds(num, t_total):
    return min(max(0, num), t_total)


def get_number_winning_options(t_total, record_distance):
    zero_points = get_zero_points(t_total, record_distance)
    # print(zero_points)
    # print(limit_to_bounds(zero_points[0], t_total))
    # print(limit_to_bounds(zero_points[1], t_total))
    if len(zero_points) == 0:
        return 0
    if len(zero_points) == 1:
        return num_integers_in_range(limit_to_bounds(zero_points[0], t_total), limit_to_bounds(zero_points[0], t_total))
    else:
        return num_integers_in_range(limit_to_bounds(zero_points[0], t_total), limit_to_bounds(zero_points[1], t_total))
    

def get_winning_count_product(records):
    return math.prod([get_number_winning_options(time, distance) for time, distance in records])

    

def get_data_from_file(filename):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]

        times = [int(num) for num in lines[0].split(':')[1].split()]
        distances = [int(num) for num in lines[1].split(':')[1].split()]
        return list(zip(times, distances))
    #     for line in file:
    #         line_string = line.rstrip()
    #         cards.append(line_to_card(line_string))
    # return cards


# print(get_number_winning_options(7, 9))
# print(get_number_winning_options(15, 40))
# print(get_number_winning_options(30, 200))

# records = get_data_from_file("input.txt")
# print(get_winning_count_product(records))

records = get_data_from_file("input_part2.txt")
print(get_number_winning_options(records[0][0], records[0][1]))
