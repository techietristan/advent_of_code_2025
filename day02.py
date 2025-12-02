with open('./day02_input.txt', 'r') as input_file:
    input_file_contents: list[str] = [ input_line.rstrip() for input_line in input_file ]

def is_dup(product_id: str) -> bool:
    product_id_length: int = len(product_id)
    if product_id_length % 2 == 1:
        return False
    first_part: str = product_id[: int(product_id_length / 2)]
    second_part: str = product_id[ - int(product_id_length / 2):]

    return bool(first_part == second_part)

ranges: list[str] = input_file_contents[0].split(',')
range_bounds: list[tuple[int, int]] = [ (int(bounds.split('-')[0]), int(bounds.split('-')[1])) for bounds in ranges ]
product_ids: list[list[str]] = [ [ str(product_id) for product_id in range(bound[0], bound[1] + 1) ] for bound in range_bounds ]

invalid_ids: list[list[int]] = [ [ int(product_id) for product_id in product_id_list if is_dup(product_id) ] for product_id_list in product_ids ]
invalid_sum: int = sum([ sum(invalid_id) for invalid_id in invalid_ids ])

# Part 1 Answer
print(invalid_sum)


def get_dup_candidates(product_id: str) -> list[str]:
    product_id_length: int = len(product_id)
    candidate_range_end: int = int(product_id_length / 2)
    dup_candidates: list[str] = [ product_id[: end + 1] 
        for end in range(candidate_range_end) 
        if product_id_length % (end + 1) == 0 ]
    
    return dup_candidates

def get_dup_product_id(product_id: str, dup: str) -> str:
    product_id_length: int = len(product_id)
    dup_length: int = len(dup)
    dup_reps: int = int(product_id_length / dup_length)
    dup_product_id: str = dup * dup_reps

    return dup_product_id

def is_dup_2(product_id: str) -> bool:
    product_id_length: int = len(product_id)
    dup_candidates: list[str] = get_dup_candidates(product_id)
    for dup_candidate in dup_candidates:
        if get_dup_product_id(product_id, dup_candidate) == product_id:
            return True

    return False
    
invalid_ids_2: list[list[int]] = [ [ int(product_id) for product_id in product_id_list if is_dup_2(product_id) ] for product_id_list in product_ids ]
invalid_sum_2: int = sum([ sum(invalid_id) for invalid_id in invalid_ids_2 ])

# Part 2 Answer
print(invalid_sum_2)