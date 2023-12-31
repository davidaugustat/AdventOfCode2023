def line_to_card(line):
    head, tail = line.split(':')
    card_number = head.split()[1]
    winning_numbers_string, my_numbers_string = tail.split('|')
    winning_numbers = [int(num) for num in winning_numbers_string.split()]
    my_numbers = [int(num) for num in my_numbers_string.split()]

    card = {
        "card_number": int(card_number),
        "winning_numbers": winning_numbers,
        "my_numbers": my_numbers
    }
    card["won_cards"] = get_num_won_cards(card)
    return card


def get_single_card_points(card):
    winning = set(card["winning_numbers"]).intersection(set(card["my_numbers"]))
    if len(winning) == 0:
        return 0
    return 2**(len(winning)-1)


def get_all_cards_points(cards):
    return sum([get_single_card_points(card) for card in cards])


def get_num_won_cards(card):
    return len(set(card["winning_numbers"]).intersection(set(card["my_numbers"])))


def find_total_card_num(cards):
    count = len(cards)
    cards_current_round = cards
    cards_next_round = []
    while len(cards_current_round) > 0:
        for card in cards_current_round:
            cards_next_round += cards[(card["card_number"]) : (card["card_number"] + card["won_cards"])]
        count += len(cards_next_round)
        cards_current_round = cards_next_round
        cards_next_round = []
    return count


def read_data_from_file(filename):
    cards = []
    with open(filename) as file:
        for line in file:
            line_string = line.rstrip()
            cards.append(line_to_card(line_string))
    return cards


# cards = read_data_from_file("testinput.txt")
cards = read_data_from_file("input.txt")
print(cards)
# print(get_all_cards_points(cards))
print(find_total_card_num(cards))