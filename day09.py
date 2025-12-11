# flake8: noqa
from dataclasses import dataclass
from shapely import Polygon # type: ignore

with open('./day09_input.txt', 'r') as input_file:
    input_file_contents: list[str] = [ input_line.strip('\n') for input_line in input_file ]

type Coord = tuple[int, int]
type Coords = tuple[Coord, Coord]

red_tiles_coords: list[Coord] = [ 
    (int(line.split(',')[0]), int(line.split(',')[1])) for line in input_file_contents
]

red_or_green_tiles: Polygon = Polygon(red_tiles_coords)

@dataclass
class Rectangle():
    coords: Coords
    
    def __post_init__(self):
        (a, b), (x, y) = self.coords
        self.area = (abs(a - x) + 1) * (abs(b - y) + 1)
        self.coords = tuple(sorted(sorted(list(self.coords), key = lambda coord: coord[0]), key = lambda coord: coord[1]))
        self.contains_only_red_or_green_tiles: bool = red_or_green_tiles.contains(Polygon(((a, b), (a, y), (x, y), (x, b))))
    
    def __repr__(self):
        return f'Coordinates: {self.coords}, Area: {self.area} Valid: {self.contains_only_red_or_green_tiles}'

    def __eq__(self, other):
        return bool(other.coords[0] in self.coords and other.coords[1] in self.coords)

    def __hash__(self):
        return hash(self.coords)

def get_all_possible_rectangles(red_tiles_coords: list[Coord]) -> list[Rectangle]:
    rectangles: list[Rectangle] = []
    for index in range(len(red_tiles_coords)):
        remaining_tiles: list[Coord] = red_tiles_coords[index + 1:]
        for tile in remaining_tiles:
            rectangle: Rectangle = Rectangle((red_tiles_coords[index], tile))
            rectangles.append(rectangle)
    sorted_rectangles: list[Rectangle] = sorted(rectangles, key = lambda rectangle: rectangle.area)

    return sorted_rectangles

possible_rectangles = get_all_possible_rectangles(red_tiles_coords)
largest_possible_rectangle: Rectangle = possible_rectangles[-1]
largest_possible_area = largest_possible_rectangle.area

# Part 1 Answer
print(largest_possible_area)

valid_rectangles: list[Rectangle] = [ rectangle for rectangle in possible_rectangles if rectangle.contains_only_red_or_green_tiles ]
largest_valid_rectangle: Rectangle = valid_rectangles[-1]
largest_valid_area = largest_valid_rectangle.area

# Part 2 Answer:
print(largest_valid_area)
