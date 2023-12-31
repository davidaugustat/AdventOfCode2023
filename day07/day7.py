from functools import cmp_to_key

five_of_a_kind = 7
four_of_a_kind = 6
full_house = 5
three_of_a_kind = 4
two_pair = 3
one_pair = 2
high_card = 1

is_part_2 = True

def frequency_of_characters(string):
    freq = {}
    for c in string:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1
    return freq


def get_hand_type(hand):
    cards = hand["cards"]
    freq = frequency_of_characters(cards)
    freq_list = list(freq.values())
    freq_list.sort(reverse=True) # highest frequency at beginning

    if freq_list[0] == 5:
        return five_of_a_kind
    if freq_list[0] == 4:
        return four_of_a_kind
    if freq_list[0] == 3:
        if freq_list[1] == 2:
            return full_house
        return three_of_a_kind
    if freq_list[0] == 2 and freq_list[1] == 2:
        return two_pair
    if freq_list[0] == 2:
        return one_pair
    if freq_list[0] == 1:
        return high_card
    
    raise Exception("Invalid card type!")


def get_best_hand_type_with_Joker(hand):
    cards = hand["cards"]
    if 'J' not in cards:
        return get_hand_type(hand)
    
    freq = frequency_of_characters(cards.replace('J', ''))
    if len(freq) == 0:
        return five_of_a_kind
    most_frequent_value = max(freq, key=freq.get)
    card_with_best_joker = cards.replace('J', most_frequent_value)
    return get_hand_type({"cards": card_with_best_joker, "bid": hand["bid"]})
    

def hand_cards_to_numbers(hand_cards):
    numbers = []
    for card in hand_cards:
        if card == "A":
            n = 14
        elif card == "K":
            n = 13
        elif card == "Q":
            n = 12
        elif card == "J":
            n = 1 if is_part_2 else 11
        elif card == "T":
            n = 10
        else:
            n = int(card)
        numbers.append(n)
    return numbers


def is_h1_greater_h2_same_type(h1, h2):
    h1_numbers = hand_cards_to_numbers(h1["cards"])
    h2_numbers = hand_cards_to_numbers(h2["cards"])

    i = 0
    while h1_numbers[i] == h2_numbers[i] and i < len(h1_numbers):
        i += 1
    return 1 if h1_numbers[i] > h2_numbers[i] else -1


def is_h1_greater_h2(h1, h2):
    if is_part_2:
        h1_type = get_best_hand_type_with_Joker(h1)
        h2_type = get_best_hand_type_with_Joker(h2)
    else:
        h1_type = get_hand_type(h1)
        h2_type = get_hand_type(h2)
    if h1_type != h2_type:
        return 1 if h1_type > h2_type else -1
    return is_h1_greater_h2_same_type(h1, h2)
    

def sort_hands_by_rank_increasing(hands):
    return sorted(hands, key=cmp_to_key(is_h1_greater_h2))


def sum_of_rewards(hands):
    hands = sort_hands_by_rank_increasing(hands)
    result = sum([(i+1) * hand["bid"] for i, hand in enumerate(hands)])
    print(result)


def read_data_from_file(filename):
    hands = []
    with open(filename) as file:
        for line in file:
            line_string = line.rstrip()
            split = line_string.split()
            hands.append({
                "cards": split[0].strip(),
                "bid": int(split[1]),
            })
            
    return hands

hands = read_data_from_file("input.txt")
# print(hands)
# hands_sorted_by_rank = sort_hands_by_rank_increasing(hands)
# print(hands_sorted_by_rank)
sum_of_rewards(hands)

# print(hand_cards_to_numbers("32T3K"))