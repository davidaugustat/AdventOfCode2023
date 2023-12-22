import matplotlib.pyplot as plt
import networkx
import math


def create_module(text: str):
    before_arrow, after_arrow = text.split(' -> ')
    module = {}
    if text[0] == '%':
        type = "ff"
        name = before_arrow[1:]
    elif text[0] == '&':
        type = "conj"
        name = before_arrow[1:]
    elif text.startswith("broadcaster"):
        type = "bc"
        name = before_arrow
    else:
        raise Exception("Invalid Type")
    
    module["type"] = type
    module["dests"] = after_arrow.split(', ')
    module["value"] = False
    return name, module


def reset_modules(modules):
    for module in modules.values():
        module["value"] = False


def draw_graph(modules: dict):
    """
    Draws a graph showing the nodes and their connections. 
    This helped me to figure out a solution for part 2.
    """
    g = networkx.Graph()
    
    for name, module in modules.items():
        successors = module["dests"]
        for s in successors:
            g.add_edge(name, s)
    
    color_map = []
    for node in g:
        if node in modules:
            color = "red" if modules[node]["type"] == "conj" else "blue"
        else:
            color = "green"
        color_map.append(color)

    networkx.draw(g, networkx.spring_layout(g), with_labels=True, node_color=color_map)
    plt.show()


def set_inputs_for_conjunctions(modules: dict):
    for module_name, module in modules.items():
        if module["type"] == "conj":
            inputs = [name for name, value in modules.items() if module_name in value["dests"]]
            module["inputs"] = {input: False for input in inputs}


def evaluate(modules: dict, init_pulse, node_to_observe="rx"):
    observed_gets_low = False

    to_process = [("broadcaster", init_pulse, None)]
    high_pulse_count = low_pulse_count = 0
    while len(to_process) > 0:
        module_name, pulse_value, pulse_source = to_process.pop(0)
        if pulse_value == True:
            high_pulse_count += 1
        else:
            low_pulse_count += 1

        # part 2:
        if module_name == node_to_observe and pulse_value == False:
            observed_gets_low = True

        if not module_name in modules:
            continue
        module = modules[module_name]
        if module["type"] == "ff":
            if pulse_value == False:
                module["value"] = not module["value"]
                to_process += [(dest, module["value"], module_name) for dest in module["dests"]]
        elif module["type"] == "conj":
            module["inputs"][pulse_source] = pulse_value
            if all(value == True for value in module["inputs"].values()):
                module["value"] = False
            else: 
                module["value"] = True
            to_process += [(dest, module["value"], module_name) for dest in module["dests"]]
        
        elif module["type"] == "bc":
            to_process += [(dest, pulse_value, module_name) for dest in module["dests"]]
    
    return high_pulse_count, low_pulse_count, observed_gets_low


def read_data_from_file(filename):
    modules = {}
    with open(filename) as file:
        for line in file:
            name, module = create_module(line.rstrip())
            modules[name] = module
    
    set_inputs_for_conjunctions(modules)
    return modules


def part1(modules):
    high_count_total = low_count_total = 0
    for _ in range(1000):
        high_count, low_count, _ = evaluate(modules, False)
        high_count_total += high_count
        low_count_total += low_count

    print("High:", high_count_total, "Low:", low_count_total)
    result = high_count_total * low_count_total
    print("Part 1 Result:", result)


def part2(modules):
    """
    The graph consists of 4 clusters which contains 12 flip flops each.
    - Each cluster is completely independent of the other clusters.
    - Each cluster's single input is directly connected to the broadcaster
    - Each cluster's output is an inverter that is connected to the central inverter
    - The output of the central inverter is directly connected to node "rx"

    As each cluster is independent, we can determine a cycle length for each cluster.
    This is the number of button presses until the cluster's output node becomes low.

    We then need to find the number of button presses until all clusters are low at the 
    same time. This is the least commmon multiple (LCM) of all cycle lengths.
    """

    central_node = next(name for name, module in modules.items() if "rx" in module["dests"])
    cluster_end_nodes = list(modules[central_node]["inputs"].keys())
    print("Central node:", central_node)
    print("Cluster outputs", cluster_end_nodes)

    cycle_lengths = []
    for cluster_end_node in cluster_end_nodes:
        button_presses = 1
        while not evaluate(modules, False, cluster_end_node)[2]:
            button_presses += 1
        cycle_lengths.append(button_presses)
        reset_modules(modules)

    print("Cycle lenghts of clusters:", cycle_lengths)

    result = math.lcm(*cycle_lengths)
    print("Part 2 Result:", result)


modules = read_data_from_file("input.txt")
# modules = read_data_from_file("testinput2.txt")
# draw_graph(modules)

part1(modules)
print()
reset_modules(modules)
part2(modules)
