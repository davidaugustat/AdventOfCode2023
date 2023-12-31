import re

def getFirstAndLastDigitNumber(line):
    digits = re.findall(r'\d', line)
    return int(digits[0] + digits[-1])

def getFirstAndLastNumberWithLetterNumbers(line):
    substitutions = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 
                     'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}

    digits = re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)
    for index, digit in enumerate(digits):
        for letters, digitValue in substitutions.items():
            if digit == letters:
                digits[index] = digitValue
    return int(digits[0] + digits[-1])


def extract_numbers(filename):
    numbers = []
    with open(filename) as file:
        for line in file:
            lineString = line.rstrip()
            number = getFirstAndLastNumberWithLetterNumbers(lineString)
            numbers.append(number)
            # numbers.append(getFirstAndLastDigitNumber(line.rstrip()))
    return numbers

numbers = extract_numbers("input.txt")
sum_nums = sum(numbers)
print(numbers)
print(f"Sum: {sum_nums}")

# example = """two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen"""

# for line in example.splitlines():
#     print(getFirstAndLastNumberWithLetterNumbers(line))