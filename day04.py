with open('./day04_input.txt', 'r') as input_file:
    input_file_contents: list[list[str]] = [ list(input_line.rstrip()) for input_line in input_file ]

def get_adjacent(coords: tuple[int, int]) -> list[tuple[int, int]]:
    row, column = coords
    offsets: list[tuple[int, int]] = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    neighbor_coords: list[tuple[int, int]] = [ (row + row_offset, column + column_offset) for row_offset, column_offset in offsets ]

    return neighbor_coords

def is_forklift_accessible(coords: tuple[int, int], diagram: list[list[str]]) -> bool:
    roll_count: int = 0
    neighbor_coords: list[tuple[int, int]] = get_adjacent(coords)
    for neighbor_coord in neighbor_coords:
        row, column = neighbor_coord
        if row >= 0 and column >= 0:
            try:
                neighbor: str = input_file_contents[row][column]
                if neighbor == '@':
                    roll_count += 1
            except IndexError:
                pass
    
    return bool(roll_count < 4)

def get_count_of_accessible_rolls(diagram: list[list[str]]):
    accessible_count: int = 0
    for row_index, row in enumerate(diagram):
        for column_index, column in enumerate(list(row)):
            coords: tuple[int,int] = (row_index, column_index)
            if diagram[row_index][column_index] == '@' and is_forklift_accessible(coords, diagram):
                accessible_count += 1
    
    return accessible_count

accessible_count: int = get_count_of_accessible_rolls(input_file_contents)

# Part 1 Answer
print(accessible_count)


def get_count_of_eventually_accessible_rolls(diagram: list[list[str]], accessible_count: int = 0) -> int:
    removed_rolls: list[tuple[int, int]] = []
    for row_index, row in enumerate(diagram):
        for column_index, column in enumerate(list(row)):
            coords: tuple[int,int] = (row_index, column_index)
            if diagram[row_index][column_index] == '@' and is_forklift_accessible(coords, diagram):
                removed_rolls.append((row_index, column_index))
                accessible_count += 1
    if not bool(removed_rolls):
        return accessible_count

    for removed_roll in removed_rolls: 
        row, column = removed_roll # type: ignore[assignment]
        diagram[row][column] = 'x' # type: ignore[call-overload]
    
    return get_count_of_eventually_accessible_rolls(diagram, accessible_count)

eventually_accessible_count: int = get_count_of_eventually_accessible_rolls(input_file_contents)

# Part 2 Answer
print(eventually_accessible_count)