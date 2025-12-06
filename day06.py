from functools import reduce

with open('./day06_input.txt', 'r') as input_file:
    input_file_contents: list[str] = [ input_line.strip('\n') for input_line in input_file ]

input_lines: list[list[int]] = [ [ int(num) for num in line.split() ] for line in input_file_contents[:-1] ]
inputs: list[list[int]] = [ 
    [ 
        input_lines[row][column]  
        for row in range(len(input_lines)) 
    ] 
    for column in range(len(input_lines[0]))
]
operations: list[str] = input_file_contents[-1].split()

def calculate(nums: list[int], oper: str, ) -> int:
    if oper == '+':
        return sum(nums)
    if oper == '*':
        return reduce(lambda x,y: x * y, nums)
    return 0

results: list[int ] = [ calculate(inputs[index], operations[index]) for index, _ in enumerate(inputs)]
sum_of_results: int = sum(results)

# Part 1 Answer
print(sum_of_results)


def get_column_start_indices(input_file_contents: list[str]) -> list[int]:
    operations_line: str = input_file_contents[-1]
    return [ index for index, char in enumerate(operations_line) if char == '+' or char == '*' ]

def get_ceph_num(input_file_contents: list[str], column: int) -> int:
    try:
        num: list[str] = [ row[column] for row in input_file_contents ]
        return int(''.join(num))
    except (ValueError, IndexError):
        return 0

def get_ceph_digits(input_file_contents: list[str], current_index: int, ceph_digits: list[int] = [], ) -> list[int]:
    next_digit: int = get_ceph_num(input_file_contents, current_index)
    if bool(next_digit):
        return get_ceph_digits(input_file_contents, current_index + 1, ceph_digits + [ next_digit ])
    return ceph_digits[::-1]

column_indices: list[int] = get_column_start_indices(input_file_contents)
ceph_digits: list[list[int]] = [ 
    get_ceph_digits(input_file_contents[:-1], current_index) 
    for current_index in column_indices 
]
ceph_results: list[int ] = [ calculate(ceph_digits[index], operations[index]) for index, _ in enumerate(ceph_digits)]
sum_of_ceph_results: int = sum(ceph_results)

# Part 2 Answer
print(sum_of_ceph_results)