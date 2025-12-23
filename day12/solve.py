def read_input(file: str):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    shapes = []
    regions = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        if ':' in line and 'x' not in line:
            shape_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() and ':' not in lines[i]:
                shape_lines.append(lines[i].rstrip())
                i += 1
            shape = parse_shape(shape_lines)
            shapes.append(shape)
        elif 'x' in line:
            parts = line.split(': ')
            w, h = map(int, parts[0].split('x'))
            counts = list(map(int, parts[1].split()))
            regions.append((w, h, counts))
            i += 1
        else:
            i += 1
    
    return shapes, regions

def parse_shape(lines):
    coords = []
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == '#':
                coords.append((r, c))
    return coords

def get_rotations_and_flips(shape):
    variants = []
    coords = shape
    
    for _ in range(4):
        normalized = normalize(coords)
        variants.append(normalized)
        coords = rotate_90(coords)
    
    coords = flip_horizontal(shape)
    for _ in range(4):
        normalized = normalize(coords)
        variants.append(normalized)
        coords = rotate_90(coords)
    
    unique = []
    seen = set()
    for v in variants:
        key = tuple(sorted(v))
        if key not in seen:
            seen.add(key)
            unique.append(v)
    
    return unique

def rotate_90(coords):
    return [(c, -r) for r, c in coords]

def flip_horizontal(coords):
    return [(r, -c) for r, c in coords]

def normalize(coords):
    if not coords:
        return coords
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return [(r - min_r, c - min_c) for r, c in coords]

def can_place(grid, shape, start_r, start_c):
    for dr, dc in shape:
        r, c = start_r + dr, start_c + dc
        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
            return False
        if grid[r][c]:
            return False
    return True

def place(grid, shape, start_r, start_c, val):
    for dr, dc in shape:
        r, c = start_r + dr, start_c + dc
        grid[r][c] = val

def solve_region(width, height, shapes, counts):
    grid = [[0] * width for _ in range(height)]
    presents = []
    
    for shape_idx, count in enumerate(counts):
        for _ in range(count):
            presents.append(shapes[shape_idx])
    
    if not presents:
        return True
    
    total_cells_needed = sum(len(p) for p in presents)
    if total_cells_needed > width * height:
        return False
    
    presents.sort(key=lambda x: len(x), reverse=True)
    
    variants_cache = {}
    for present in presents:
        key = tuple(sorted(present))
        if key not in variants_cache:
            variants_cache[key] = get_rotations_and_flips(present)
    
    def backtrack(present_idx):
        if present_idx == len(presents):
            return True
        
        key = tuple(sorted(presents[present_idx]))
        shape_variants = variants_cache[key]
        
        for r in range(height):
            for c in range(width):
                if grid[r][c] == 0:
                    for variant in shape_variants:
                        if can_place(grid, variant, r, c):
                            place(grid, variant, r, c, present_idx + 1)
                            if backtrack(present_idx + 1):
                                return True
                            place(grid, variant, r, c, 0)
        
        return False
    
    return backtrack(0)

def solve1(shapes, regions):
    count = 0
    for width, height, counts in regions:
        if solve_region(width, height, shapes, counts):
            count += 1
    return count

if __name__ == "__main__":
    shapes, regions = read_input('input')
    print(solve1(shapes, regions))
