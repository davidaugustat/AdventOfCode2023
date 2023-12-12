import math

"""
Notes on part 2:

I observed that
- From each A-node only one single Z-node is reachable (not multiple)
- Number of steps from A-node to Z-node equals number of steps from Z-node to same Z-node
- This is indepentent of the position in the instruction cycle

--> Each A-node n_i has a fixed cycle length l_i (int) such that a z-node is reached exactly at
the steps
step = k_i * l_i
for every integer k_i > 0

Thus, we need to find integers k_0, ..., k_m > 0 (for m A-nodes) such that
k_0 * l_0 = k_1 * l_1 = ... = k_m * l_m
and k_0 * l_0 minimal
--> Use least common multiple (lcm)!
"""

def follow_path(instructions, nodes, start_node='AAA', end_node='ZZZ'):
    count = 0
    current_node = start_node
    while current_node != end_node:
        instruction = instructions[count % len(instructions)]
        current_node = nodes[current_node][instruction]
        count += 1
    return count


def follow_path_until_Z_at_end(instructions, nodes, start_node):
    count = 0
    current_node = start_node
    while not current_node.endswith('Z'):
        instruction = instructions[count % len(instructions)]
        current_node = nodes[current_node][instruction]
        count += 1
    return count


def get_cycle_lengths(instructions, nodes, start_nodes):
    cycle_lengths = []
    for start_node in start_nodes:
        cycle_length = follow_path_until_Z_at_end(instructions, nodes, start_node)
        cycle_lengths.append(cycle_length)
    return cycle_lengths


def part_two_lcm(instructions, nodes):
    start_nodes = get_nodes_ending_with_A(nodes)
    cycle_lengths = get_cycle_lengths(instructions, nodes, start_nodes)
    lcm = math.lcm(*cycle_lengths)
    print(f"Count: {lcm}")
    

def get_nodes_ending_with_A(nodes):
    return list(filter(lambda node_name: node_name.endswith('A'), nodes.keys()))


def read_data_from_file(filename):
    instructions = []
    nodes = {}
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
        instructions = [0 if c == 'L' else 1 for c in lines[0]]
        node_lines = lines[2:]
        for node_line in node_lines:
            lhs, rhs = node_line.split('=')
            node_name = lhs.strip()
            rhs = rhs.replace('(', '')
            rhs = rhs.replace(')', '')
            left_node, right_node = rhs.split(',')
            left_node = left_node.strip()
            right_node = right_node.strip()
            nodes[node_name] = [left_node, right_node]

            
    return instructions, nodes

# instructions, nodes = read_data_from_file("testinput1.txt")
# instructions, nodes = read_data_from_file("testinput2.txt")
instructions, nodes = read_data_from_file("input.txt")

# Part 1
num_steps = follow_path(instructions, nodes)
print(num_steps)

# Part 2
part_two_lcm(instructions, nodes)
