import re
import copy

def parse_part(part_string):
    part = {}
    part_string = part_string[1:-1] # remove curly brackets
    kv_pairs_strings = part_string.split(',')
    for kv_pair_string in kv_pairs_strings:
        key, value = kv_pair_string.split('=')
        part[key] = int(value)
    return part


def parse_workflow(workflow_string):
    workflow = {}

    workflow_string = workflow_string[0:-1] # remove closing curly brace
    name, all_instructions_string  =workflow_string.split('{')
    instructions_strings = all_instructions_string.split(',')

    instructions = []
    for instruction_string in instructions_strings:
        instruction = {}
        if ':' in instruction_string:
            instruction["type"] = "cond"
            variable, operator, value, _, target = re.split("(<|>|:)", instruction_string)
            instruction["var"] = variable
            instruction["operator"] = operator
            instruction["value"] = int(value)
            instruction["target"] = target

        elif instruction_string == 'A':
            instruction["type"] = "accept"
        elif instruction_string == "R":
            instruction["type"] = "reject"
        else:
            instruction["type"] = "forward"
            instruction["target"] = instruction_string
        
        instructions.append(instruction)
    
    workflow["instructions"] = instructions
    return name, workflow


def test_part(part, workflows):
    current_workflow = workflows["in"]
    while True:
        for instruction in current_workflow["instructions"]:
            type = instruction["type"] 
            if type == "accept":
                return True
            elif type == "reject":
                return False
            elif type == "forward":
                current_workflow = workflows[instruction["target"]]
                break
            elif type == "cond":
                if instruction["operator"] == '<' and part[instruction["var"]] < instruction["value"] \
                    or instruction["operator"] == '>' and part[instruction["var"]] > instruction["value"]:
                    if instruction["target"] == 'A':
                        return True
                    elif instruction["target"] == 'R':
                        return False
                    else:
                        current_workflow = workflows[instruction["target"]]
                    break
            else:
                raise Exception("Invalid instruction type")

            
def split_range(input_range, operator, value):
    min_val, max_val = input_range
    if operator == '<':
        range_a = (min_val, min(max_val, value - 1)) if value > min_val else None
        range_b = (max(min_val, value), max_val) if value <= max_val else None
    elif operator == '>':
        range_b = (min_val, min(max_val, value)) if value >= min_val else None
        range_a = (max(min_val, value + 1), max_val) if value < max_val else None
    else:
        raise ValueError("Operator must be '<' or '>'")

    return range_a, range_b


def find_accepted_range_pairs(workflows):
    accepted = []
    to_check = [{"start":"in", "x":(1,4000), "m":(1,4000), "a":(1,4000), "s":(1,4000)}]

    while len(to_check) > 0:
        range_pair = to_check.pop()
        workflow = workflows[range_pair["start"]]
        for instruction in workflow["instructions"]:
            type = instruction["type"]
            if type == "accept":
                accepted.append(range_pair)
                break
            elif type == "reject":
                break
            elif type == "forward":
                range_pair["start"] = instruction["target"]
                to_check.append(range_pair)
                break
            elif type == "cond":
                matching_range, rest_range = split_range(range_pair[instruction["var"]], instruction["operator"], instruction["value"])
                if matching_range != None:
                    new_range_pair = copy.deepcopy(range_pair)
                    new_range_pair[instruction["var"]] = matching_range
                    if instruction["target"] == "A":
                        accepted.append(new_range_pair)
                    elif instruction["target"] == "R":
                        pass # nothing to do
                    else:
                        new_range_pair["start"] = instruction["target"]
                        to_check.append(new_range_pair)                       
                if rest_range != None:
                    range_pair[instruction["var"]] = rest_range
                else:
                    break
    return accepted


def calc_combinations_from_ranges(accepted_ranges):
    result = 0
    for r in accepted_ranges:
        result += (r["x"][1] - r["x"][0] + 1) * (r["m"][1] - r["m"][0] + 1) * (r["a"][1] - r["a"][0] + 1) * (r["s"][1] - r["s"][0] + 1)
    return result


def part1(workflows, parts):
    accepted_parts = [part for part in parts if test_part(part, workflows)]
    result = sum(sum(part.values()) for part in accepted_parts)
    print("Part 1 Result:", result)


def part2(workflows):
    accepted_ranges = find_accepted_range_pairs(workflows)
    result = calc_combinations_from_ranges(accepted_ranges)
    print("Part 2 Result:", result)


def read_data_from_file(filename):
    workflows = {}
    parts = []

    with open(filename) as file:
        is_parts_section = False
        for line in file:
            if line == '\n':
                is_parts_section = True
                continue
            if not is_parts_section:
                name, workflow = parse_workflow(line.rstrip())
                workflows[name] = workflow
            else: 
                parts.append(parse_part(line.rstrip()))
    return workflows, parts


# workflows, parts = read_data_from_file("testinput.txt")
workflows, parts = read_data_from_file("input.txt")

part1(workflows, parts)
part2(workflows)
