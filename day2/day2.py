def parseGame(line):
    game, data = line.split(':')
    id = int(game.split(' ')[1])
    set_strings = data.split(';')

    game_data = {
        "id": id,
        "sets": []
    }

    for set_string in set_strings:
        current_set = {}
        color_info_strings = set_string.split(',')
        for color_info_string in color_info_strings:
            count, color = color_info_string.strip().split(' ')
            current_set[color] = int(count)
        game_data["sets"].append(current_set)

    return game_data
        

def filter_game_ids(games, max_red, max_green, max_blue):
    valid_ids = []

    for game in games:
        valid = True
        for game_set in game["sets"]:
            if game_set.get("red",0) > max_red or game_set.get("green",0) > max_green or game_set.get("blue",0) > max_blue:
                valid = False
        if valid:
            valid_ids.append(game["id"])
    return valid_ids


def get_min_set_of_cubes_power(game):
    sets = game["sets"]
    min_red = max(map(lambda current_set : current_set.get("red",0), sets))
    min_green = max(map(lambda current_set : current_set.get("green",0), sets))
    min_blue = max(map(lambda current_set : current_set.get("blue",0), sets))
    return min_red * min_green * min_blue


def readDataFromFile(filename):
    games = []
    with open(filename) as file:
        for line in file:
            lineString = line.rstrip()
            games.append(parseGame(lineString))
    return games

games = readDataFromFile("input.txt")

# ids = filter_game_ids(games, 12, 13, 14)
# print(sum(ids))

sum_of_powers = sum([get_min_set_of_cubes_power(game) for game in games])
print(sum_of_powers)

# g1 = "Game 1: 1 red, 5 blue, 10 green; 5 green, 6 blue, 12 red; 4 red, 10 blue, 4 green"
# print(parseGame(g1))

