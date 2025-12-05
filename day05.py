with open('./day05_input.txt', 'r') as input_file:
    input_file_contents: list[str] = [ input_line.rstrip() for input_line in input_file ]

def get_range(id_range: str) -> range:
    start, end = id_range.split('-')
    
    return range(int(start), int(end) + 1)

def is_fresh(ingredient_id: int, fresh_ranges: list[range]) -> bool:
    for fresh_range in fresh_ranges:
        if ingredient_id in fresh_range:
            return True
    return False

fresh_ranges: list[range] = [ get_range(line) for line in input_file_contents if '-' in line ]
ingredient_ids: list[int] = [ int(id) for id in input_file_contents if '-' not in id and bool(id) ]
fresh_ingredient_ids: list [int] = [ ingredient_id for ingredient_id in ingredient_ids if is_fresh(ingredient_id, fresh_ranges) ]
count_of_fresh_ingredients: int = len(fresh_ingredient_ids)

# Part 1 Answer
print(count_of_fresh_ingredients)


def ranges_overlap(first_range: range, second_range: range) -> bool:
    return bool(first_range.start <= second_range.stop and second_range.start <= first_range.stop)

def get_merged_range(first_range: range, second_range: range) -> range:
    merged_range_start: int = min(first_range.start, second_range.start)
    merged_range_stop: int = max(first_range.stop, second_range.stop)
    merged_range: range = range(merged_range_start, merged_range_stop)

    return merged_range

def get_sorted_fresh_ranges(fresh_ranges: list[range]) -> list[range]:
    fresh_ranges_by_stop: list[range] = sorted(
        [ fresh_range for fresh_range in fresh_ranges ], 
        key = lambda fresh_range: fresh_range.stop )
    fresh_ranges_by_start: list[range] = sorted(
        [ fresh_range for fresh_range in fresh_ranges_by_stop ], 
        key = lambda fresh_range: fresh_range.start )

    return fresh_ranges_by_start

def merge_fresh_ranges(
    sorted_unmerged_ranges: list[range],
    merged_ranges: list[range] = [], 
    ) -> list[range]:
    if not bool(sorted_unmerged_ranges):
        return merged_ranges

    current_range = sorted_unmerged_ranges[0]
    merged_indices: list[int] = [0]

    for index, merge_candidate in enumerate(sorted_unmerged_ranges):
        if ranges_overlap(current_range, merge_candidate):
            merged_range: range = get_merged_range(current_range, merge_candidate)
            current_range = merged_range
            merged_indices = merged_indices + [ index ]
    
    merged_ranges = merged_ranges + [ current_range ]
    sorted_unmerged_ranges = [ fresh_range for index, fresh_range 
        in enumerate(sorted_unmerged_ranges) 
        if index not in merged_indices]

    return merge_fresh_ranges(sorted_unmerged_ranges, merged_ranges)


sorted_fresh_ranges: list[range] = get_sorted_fresh_ranges(fresh_ranges)
merged_fresh_ranges: list[range] = merge_fresh_ranges(sorted_fresh_ranges)
range_lengths: list[int] = [ len(fresh_range) for fresh_range in merged_fresh_ranges ]
total_fresh_item_ids: int = sum(range_lengths)

# Part 2 Answer
print(total_fresh_item_ids)