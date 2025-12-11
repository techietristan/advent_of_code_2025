# flake8: noqa

from dataclasses import dataclass
from functools import reduce
from math import sqrt
from sys import setrecursionlimit
import time

start_time = time.time()

with open('./day08_input.txt', 'r') as input_file:
    input_file_contents: list[str] = [ input_line.strip('\n') for input_line in input_file ]

CONNECTIONS: int = 1000
NUMBER_OF_CIRCUITS_TO_MULTIPLY: int = 3

setrecursionlimit( len(input_file_contents) * 10)

type Coord = tuple[int, int, int]
type Coords = tuple[Coord, Coord]

def get_distance(coords_1: Coord, coords_2: Coord) -> float:
    a, b, c = coords_1
    x, y, z = coords_2
    distance: float = sqrt((a - x)**2 + (b - y)**2 + (c - z)**2)

    return float(distance)

@dataclass
class Connection():
    coords: Coords
    distance: float = float('inf')

    def __post_init__(self):
        self.coords = tuple(sorted(list(self.coords), key = lambda coord: coord[0]))
        self.distance = get_distance(self.coords[0], self.coords[1])
    
    def __hash__(self):
        return hash((self.coords, self.distance))

    def __eq__(self, other):
        return bool(other.coords == self.coords)

    def __repr__(self):
        return f'{self.coords[0]}, {self.coords[1]}, {self.distance}'
    
@dataclass
class Circuit():
    id: int
    junction_boxes: list[Coord]

    def __post_init__(self):
        self.junction_boxes = sorted(list(set(self.junction_boxes)), key = lambda coords: coords[0])

    def circuit_size(self) -> int:
        return int(len(self.junction_boxes))

    def contains(self, junction_box: Coord) -> bool:
        return bool(junction_box in self.junction_boxes)
    
    def connect(self, junction_box: Coord):
        return Circuit(self.id, self.junction_boxes + [ junction_box ])

def get_sorted_connections(connections: set[Connection]) -> tuple[Connection, ...]:
    sorted_connections: tuple[Connection, ...] = tuple(sorted(list(connections), key = lambda pair: pair.distance))

    return sorted_connections

def get_circuits(sorted_connections: tuple[Connection, ...], junction_boxes: list[Coord], connected_junction_boxes: list[Coord] = [], circuits: list[Circuit] = [], circuits_after_x_iterations: list[Circuit] = [], index = 0) -> tuple[list[Circuit], Coords]: # type: ignore
    if index == CONNECTIONS:
        circuits_after_x_iterations = circuits
    if len(connected_junction_boxes) == len(junction_boxes):
        final_coords: Coords = sorted_connections[index - 1].coords
        return circuits_after_x_iterations, final_coords

    connection: Connection = sorted_connections[index]
    box1, box2 = connection.coords

    if not circuits:
        connected_junction_boxes = [ box1, box2 ]
        circuits = [ Circuit(index, connected_junction_boxes) ]
        return get_circuits(sorted_connections, junction_boxes, connected_junction_boxes, circuits, circuits_after_x_iterations, index + 1)

    box1_circuit_id: tuple[int, int] | bool = False if box1 not in connected_junction_boxes else [ (index, circuit.id) for index, circuit in enumerate(circuits) if circuit.contains(box1) ][0] 
    box2_circuit_id: tuple[int, int] | bool = False if box2 not in connected_junction_boxes else [ (index, circuit.id) for index, circuit in enumerate(circuits) if circuit.contains(box2) ][0] 

    if box1 in connected_junction_boxes and box2 in connected_junction_boxes:
        new_circuit_id: int = min(box1_circuit_id[1], box2_circuit_id[1]) # type: ignore
        existing_junction_boxes: list[Coord] = circuits[box1_circuit_id[0]].junction_boxes + circuits[box2_circuit_id[0]].junction_boxes # type: ignore
        new_circuit: Circuit = Circuit(new_circuit_id, existing_junction_boxes + [ box1, box2 ] )
        updated_circuits: list[Circuit] = sorted([ new_circuit ] + [ circuit for circuit in circuits if circuit.id not in [ box1_circuit_id[1], box2_circuit_id[1] ]], key = lambda circuit: circuit.id ) # type: ignore
        connected_junction_boxes = list(set(connected_junction_boxes + [ box1, box2]))
        return get_circuits(sorted_connections, junction_boxes, connected_junction_boxes, updated_circuits, circuits_after_x_iterations, index + 1)
    
    if box1 in connected_junction_boxes and box2 not in connected_junction_boxes:
        updated_circuit = circuits[box1_circuit_id[0]].connect(box2) # type: ignore
        updated_circuits = sorted([ updated_circuit ] + [ circuit for circuit in circuits if circuit.id != box1_circuit_id[1] ], key = lambda circuit: circuit.id ) # type: ignore
        connected_junction_boxes = list(set(connected_junction_boxes + [ box2 ]))
        return get_circuits(sorted_connections, junction_boxes, connected_junction_boxes, updated_circuits, circuits_after_x_iterations, index + 1)
    
    if box2 in connected_junction_boxes and box1 not in connected_junction_boxes:
        updated_circuit = circuits[box2_circuit_id[0]].connect(box1) # type: ignore
        updated_circuits = sorted([ updated_circuit ] + [ circuit for circuit in circuits if circuit.id != box2_circuit_id[1] ], key = lambda circuit: circuit.id ) # type: ignore
        connected_junction_boxes = list(set(connected_junction_boxes + [ box1 ]))
        return get_circuits(sorted_connections, junction_boxes, connected_junction_boxes, updated_circuits, circuits_after_x_iterations, index + 1)
    
    if box1 not in connected_junction_boxes and box1 not in connected_junction_boxes:
        new_circuit = Circuit(index, [ box1, box2] )
        updated_circuits = sorted(circuits + [ new_circuit ], key = lambda circuit: circuit.id )
        connected_junction_boxes = list(set(connected_junction_boxes + [ box1, box2]))
        return get_circuits(sorted_connections, junction_boxes, connected_junction_boxes, updated_circuits, circuits_after_x_iterations, index + 1)

def get_multiple_of_largest_circuit_sizes(circuits: list[Circuit], number_of_circuits: int = 3) -> int:
    largest_circuits: list[Circuit] = sorted(circuits, key = lambda circuit: circuit.circuit_size(), reverse = True)[:3]
    largest_circuit_sizes: list[int] = [ circuit.circuit_size() for circuit in largest_circuits ]
    multiple_of_largest_circuit_sizes = reduce(lambda x, y: x * y, largest_circuit_sizes)

    return multiple_of_largest_circuit_sizes

junction_boxes: list[Coord] = sorted([ 
    tuple([ int(coord) for coord in junction_box.split(',') ]) # type: ignore
    for junction_box in input_file_contents ],
    key = lambda x: x[0])

connections: set[Connection] = set(
    Connection((coords_1, coords_2))
    for coords_1 in junction_boxes
    for coords_2 in junction_boxes
    if coords_1 != coords_2
)

sorted_connections: tuple[Connection, ...] = get_sorted_connections(connections)
circuits_after_x_iterations, final_coords = get_circuits(sorted_connections, junction_boxes)
multiple_of_largest_circuit_sizes = get_multiple_of_largest_circuit_sizes(circuits_after_x_iterations, NUMBER_OF_CIRCUITS_TO_MULTIPLY)

# Part 1 Answer
print(multiple_of_largest_circuit_sizes)

x_coords_of_final_circuits: tuple[int, int] = final_coords[0][0], final_coords[1][0]
product_of_final_x_coords: int = x_coords_of_final_circuits[0] * x_coords_of_final_circuits[1]

# Part 2 Answer
print(product_of_final_x_coords)