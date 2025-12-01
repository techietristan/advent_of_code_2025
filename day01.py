from math import floor

with open('./day01_input.txt', 'r') as input_file:
    input_file_contents: list[str] = [ input_line.rstrip() for input_line in input_file ]

current_position: int = 50
zero_count: int = 0


def get_zero_count(current_position: int, change: int) -> int:
    next_position: int = current_position + change
    if current_position == 0 or next_position > 99:
        return floor(abs(next_position) / 100)
    if next_position == 0:
        return floor(abs(next_position) / 100) + 1
    if next_position <= 0:
        return floor((abs(next_position) + 100) / 100)
    return 0


def get_next_position(dial_move: str) -> int:
    global current_position
    global zero_count
    distance: int = int(dial_move[1:])
    change: int = distance if dial_move[0] == 'R' else - distance
    next_position: int = current_position + change

    if 0 <= next_position < 100:
        dial_position = next_position
        zero_count += get_zero_count(current_position, change)
    elif next_position > 99:
        dial_position = next_position % 100
        zero_count += get_zero_count(current_position, change)
    else:
        dial_position = (100 + next_position) % 100
        zero_count += get_zero_count(current_position, change)

    current_position = dial_position

    return dial_position


dial_positions: list[int] = [get_next_position(dial_move) for dial_move in input_file_contents]
password: int = dial_positions.count(0)

# Part 1 Answer
print(password)

# Part 2 Answer
print(zero_count)