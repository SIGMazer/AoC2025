
def read_input(file:str) -> list:
    with open(file, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def part1(grid: list) -> int:
    result: int = 0 

    # find @ in grid and look for adjacent @ in 4 directions and diagonal
    # if the adjacent count < 4 then increase result by 1
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                adjacent_count = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                        adjacent_count += 1
                if adjacent_count < 4:
                    result += 1
    return result

def find_adjacent_count(grid: list, r: int, c: int) -> int:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    adjacent_count = 0
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
            adjacent_count += 1
    return adjacent_count

def part2(grid: list) -> int:
    result: int = 0 

    # find @ in grid and look for adjacent @ in 4 directions and diagonal
    # if the adjacent count < 4 then increase result by 1 and remove that @ from grid
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    while True:
        result_old = result

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@':
                    adjacent_count = find_adjacent_count(grid, r, c)
                    if adjacent_count < 4:
                        result += 1
                        grid[r] = grid[r][:c] + '.' + grid[r][c+1:]
        if result == result_old:
            break
    return result

if __name__ == "__main__":
    grid = read_input('input')
    print(part2(grid))


