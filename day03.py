with open('./day03_input.txt', 'r') as input_file:
    input_file_contents: list[str] = [ input_line.rstrip() for input_line in input_file ]

battery_banks: list[list[int]] = [ [ int(digit) for digit in list(line) ] for line in input_file_contents ]

def get_highest_possible_joltage(battery_bank: list[int]) -> int:
    highest_possible_joltage: int = 0
    for index, battery in enumerate(battery_bank, 1):
        possible_pairings: list[int] = battery_bank[index:]
        for possible_pairing in possible_pairings:
            pairing_joltage: int = int(f'{battery}{possible_pairing}')
            if pairing_joltage > highest_possible_joltage:
                highest_possible_joltage = pairing_joltage
    
    return highest_possible_joltage

highest_possible_joltages: list[int] = [ get_highest_possible_joltage(battery_bank) for battery_bank in battery_banks ]
sum_of_highest_posssible_joltages: int = sum(highest_possible_joltages)

# Part 1 Answer
print(sum_of_highest_posssible_joltages)


BANK_SIZE: int = 12

def get_highest_possible_joltage_bank(
    battery_bank: list[int],
    active_batteries: list[int] = [],
    window_start: int = 0,
    window_end: int = - BANK_SIZE + 1
    ) -> list[int]:
    if len(active_batteries) == BANK_SIZE:
        return active_batteries

    search_window: list[int] = battery_bank[window_start: window_end]
    max_battery_in_window: int = max(search_window)
    max_battery_window_index: int = search_window.index(max_battery_in_window)
    max_battery_bank_index: int = max_battery_window_index + window_start
    active_batteries = active_batteries + [ max_battery_in_window ]
    next_window_start: int = max_battery_bank_index + 1
    next_window_end: int = len(battery_bank) - (BANK_SIZE - len(active_batteries)) + 1

    return get_highest_possible_joltage_bank(
        battery_bank,
        active_batteries,
        next_window_start,
        next_window_end
    )

highest_possible_joltage_battery_banks: list[list[int]] = [ get_highest_possible_joltage_bank(battery_bank) for battery_bank in battery_banks ]
battery_bank_joltages: list[int] = [ 
    int(''.join([ str(digit) for digit in battery_bank ])) 
    for battery_bank in highest_possible_joltage_battery_banks
]
sum_of_highest_possible_joltage_battery_banks: int = sum(battery_bank_joltages)

# Part 2 Answer
print(sum_of_highest_possible_joltage_battery_banks)