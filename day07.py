from dataclasses import dataclass

with open('./day07_input.txt', 'r') as input_file:
    input_file_contents: list[list[str]] = [ list(input_line.rstrip()) for input_line in input_file ]

def get_beam_origin(manifold: list[list[str]]) -> tuple[int, int]:
    for row_index, row in enumerate(manifold):
        for char_index, char in enumerate(row):
            if char == 'S':
                beam_origin: tuple[int, int] = (row_index, char_index)
                break

    return beam_origin

def get_total_splits(manifold: list[list[str]], coords: list[tuple[int, int]], split_locations: list[tuple[int, int]] = []) -> int:
    if not bool(coords):
        total_splits: int = len(set(split_locations))
        return total_splits 
    next_coords: list[tuple[int, int]] = []
    for coord in coords:
        current_row, current_column = coord
        current_char: str = manifold[current_row][current_column]
        if current_char == '.':
            manifold[current_row][current_column] = '|'
        next_coord = (current_row + 1, current_column)
        row, column = next_coord
        try:
            next_location: str = manifold[row][column]
            if next_location == '.':
                next_coords = next_coords + [ next_coord ]
            if next_location == '^':
                split_locations = split_locations + [ next_coord ]
                split_coords: list[tuple[int, int]] = [ (row, column - 1), (row, column + 1) ]
                next_coords = next_coords + [ (row + 1, column - 1), (row + 1, column + 1) ]
                for split_coord in split_coords:
                    split_row, split_column = split_coord
                    if manifold[split_row][split_column] == '.':
                        manifold[split_row][split_column] = '|'
        except IndexError:
            continue

    return get_total_splits(manifold, list(set(next_coords)), split_locations)

beam_origin: tuple[int, int] = get_beam_origin(input_file_contents)
total_splits: int = get_total_splits(input_file_contents, [ beam_origin ])

# Part 1 Answer
print(total_splits)


@dataclass
class Beam:
    coords: tuple[int, int]
    timelines: int = 1

    def __eq__(self, other):
        return self.coords == other.coords

    def row(self) -> int:
        return self.coords[0]
    
    def next(self) -> tuple[int, int]:
        row, column = self.coords
        return (row + 1, column)
    
    def twins(self):
        row, column = self.coords
        left = Beam((row + 1, column - 1), self.timelines)
        right = Beam((row + 1, column + 1), self.timelines)
        return [ left, right ]

    def increment(self, amount: int = 1):
        self.timelines += amount

def get_potential_split_locations(manifold: list[list[str]]) -> list[tuple[int, int]]:
    potential_split_locations: list[tuple[int, int]] = [
        (row, column) for row in range(len(manifold))
        for column in range(len(manifold[0]))
        if manifold[row][column] == '^'
    ]
    
    return potential_split_locations

potential_split_locations = get_potential_split_locations(input_file_contents)
manifold_size: int = len(input_file_contents)

def get_timeline_count(beams: list[Beam], current_row: int = 0) -> int:
    if current_row == manifold_size:
        timelines: int = sum([ beam.timelines for beam in beams if beam.row() == current_row - 1 ])
        return timelines
    for beam in beams:
        if beam.row() == current_row:
            if beam.next() in potential_split_locations:
                twins: list[Beam] = beam.twins()
                for twin in twins:
                    if twin in beams:
                        beams[beams.index(twin)].increment(beam.timelines)
                    else:
                        beams += [ twin ]
            else:
                next_beam: Beam = Beam(beam.next(), beam.timelines)
                if next_beam in beams:
                    beams[beams.index(next_beam)].increment(beam.timelines)
                else:
                    beams += [ next_beam ]

    return get_timeline_count(beams, current_row + 1)


beam_row, beam_column = (beam_origin[0] + 1, beam_origin[1])
initial_beam: Beam = Beam((beam_row, beam_column))
timeline_count: int = get_timeline_count([ initial_beam ], 1)

# Part 2 Answer
print(timeline_count)