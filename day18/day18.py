from shapely.geometry import Polygon

def dig_by_plan(plan):
    points = [(0,0)]
    for dir, meters, color in plan:
        x_prev, y_prev = points[-1]
        # meters += 1
        if dir == "L":
            x = x_prev - meters
            y = y_prev
        elif dir == "R":
            x = x_prev + meters
            y = y_prev
        elif dir == "U":
            x = x_prev
            y = y_prev - meters
        elif dir == "D":
            x = x_prev
            y = y_prev + meters
        points.append((x,y))
    return points


# def dig_by_plan2(plan):
#     points_a = [(0,0)]
#     points_b = []
#     for dir, meters, color in plan:
#         x_prev, y_prev = points[-1]
#         # meters += 1
#         if dir == "L":
#             x = x_prev - meters
#             y = y_prev
#         elif dir == "R":
#             x = x_prev + meters
#             y = y_prev
#         elif dir == "U":
#             x = x_prev
#             y = y_prev - meters
#         elif dir == "D":
#             x = x_prev
#             y = y_prev + meters
#         points.append((x,y))
#     return points

# def dig_by_plan2(plan):

def get_pos_after_step(pos, dir):
    x_prev, y_prev = pos
    if dir == "L":
        x = x_prev - 1
        y = y_prev
    elif dir == "R":
        x = x_prev + 1
        y = y_prev
    elif dir == "U":
        x = x_prev
        y = y_prev - 1
    elif dir == "D":
        x = x_prev
        y = y_prev + 1
    return (x, y)


def dig_by_plan3(plan):
    marked = {}
    current_pos = (0,0)
    marked[current_pos] = True
    
    for dir, meters, color in plan:
        # x_prev, y_prev = current_pos
        # if dir == "L":
        #     x = x_prev - meters
        #     y = y_prev
        # elif dir == "R":
        #     x = x_prev + meters
        #     y = y_prev
        # elif dir == "U":
        #     x = x_prev
        #     y = y_prev - meters
        # elif dir == "D":
        #     x = x_prev
        #     y = y_prev + meters

        for _ in range(meters):
            current_pos = get_pos_after_step(current_pos, dir)
            marked[current_pos] = True
    
    return marked


def dig_by_plan4(plan):
    prev_a_x, prev_a_y = 0 ,0 # todo
    prev_b_x, prev_b_y = 0 ,0 # todo
    poly_a = [(prev_a_x, prev_a_y)]
    poly_b = [(prev_b_x, prev_b_y)]
    prev_dir = plan[-1][0]

    for dir, meters, color in plan:
        if prev_dir == "L":
            if dir == "U":
                
            elif dir == "D":

        

def get_area2(marked):
    outline = list(marked.keys())
    min_x = min(point[0] for point in outline)
    min_y = min(point[1] for point in outline)
    max_x = max(point[0] for point in outline)
    max_y = max(point[1] for point in outline)

    outside = {(min_x -1, min_y -1)}
    change = True
    while change:
        change = False
        for y in range(min_y-1, max_y+1+1):
            for x in range(min_x-1, max_x+1+1):
                if not marked.get((x,y), False):
                    if ((x-1,y) in outside or (x+1,y) in outside or (x,y-1) in outside or (x,y+1) in outside) and (x,y) not in outside:
                        outside.add((x,y))
                        change = True
    
    # print(min_x, min_y, max_x, max_y)
    # print(len(outside))
    area = ((max_x + 1 + 1) - (min_x - 1)) * ((max_y + 1 + 1) - (min_y - 1)) - len(outside)
    return area

def get_area(marked):
    outline = list(marked.keys())
    min_x = min(point[0] for point in outline)
    min_y = min(point[1] for point in outline)
    max_x = max(point[0] for point in outline)
    max_y = max(point[1] for point in outline)

    area = 0
    for y in range(min_y, max_y+1):
        inside_area = False
        for x in range(min_x, max_x+1):
            # if not inside_area and marked.get((x,y), False) and not marked.get((x+1,y), False):
            #     inside_area = True
            if inside_area or marked.get((x,y), False):
                area += 1

            

            # if inside_area:
            #     area += 1

            if not inside_area and marked.get((x,y), False) and not marked.get((x+1,y), False):
                inside_area = True
            elif inside_area and marked.get((x,y), False) and not marked.get((x+1,y), False):
                inside_area = False

    return area
        





def get_polygon_area(points):
    return Polygon(points).area


def part1(plan):
    points = dig_by_plan(plan)
    print([(point[1], point[0]) for point in points])
    area = get_polygon_area(points)
    print("Part 1 Result:", area)


def adjust_from_color_codes(plan):
     for i in range(len(plan)):
        color_code = plan[i][2]
        meters = int(color_code[1:-1], 16)
        dir_num = int(color_code[-1], 16)
        dir = ["R", "D", "L", "U"][dir_num]
        plan[i] = (dir, meters, color_code)



def read_data_from_file(filename):
    plan = []
    with open(filename) as file:
        # grid = [line.rstrip() for line in file]
        # return grid
        for line in file:
            dir, meters_str, color_str = line.rstrip().split()
            color_str = color_str.replace("(", "").replace(")", "")
            plan.append((dir, int(meters_str), color_str))
    return plan

# plan = read_data_from_file("input.txt")
plan = read_data_from_file("testinput.txt")
# print(plan)
# part1(plan)
# marked = dig_by_plan3(plan)
# print(list(marked.keys()))
# print(get_polygon_area(list(marked.keys())))
# print(get_area2(marked))

adjust_from_color_codes(plan)
print(plan)

# result part 1: result < 77300 (your anser is too high)