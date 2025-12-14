
# read ranges and the ingridients from the input file

def read_input(file: str) -> tuple[list[tuple[int,int]], list[int]]:
    with open(file, 'r') as f:
        lines = f.readlines()
    ranges: list[tuple[int, int]] = []
    ingredients: list = []
    reading_ranges = True
    for line in lines:
        line = line.strip()
        if line == "":
            reading_ranges = False
            continue
        if reading_ranges:
            start, end = line.split('-')
            ranges.append((int(start), int(end)))
        else:
            ingredients.append(int(line))
    return ranges, ingredients
    
def solve1(ranges: list[tuple[int,int]], ingredients: list[int]) -> int:
    fresh = 0
    for ingredient in ingredients:
        for start, end in ranges:
            if start <= ingredient <= end:
                fresh += 1
                break
    return fresh

def solve2(ranges: list[tuple[int,int]]) -> int:
    merged_ranges: list[tuple[int, int]] = []
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    
    for current in sorted_ranges:
        if not merged_ranges:
            merged_ranges.append(current)
        else:
            last_start, last_end = merged_ranges[-1]
            current_start, current_end = current
            if current_start <= last_end + 1:
                merged_ranges[-1] = (last_start, max(last_end, current_end))
            else:
                merged_ranges.append(current)
    
    total_fresh = 0
    for start, end in merged_ranges:
        total_fresh += (end - start + 1)
    
    return total_fresh


if __name__ == "__main__":
    ranges, ingredients = read_input('input')
    result = solve2(ranges)
    print(f"Number of fresh ingredients: {result}")
