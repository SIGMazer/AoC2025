from shapely import Polygon

def read_input(file: str) -> list[tuple[int, int]]:
    with open(file, 'r') as f:
        lines = f.readlines()

    red_tiles: list[tuple[int, int]] = [(int(line.split(',')[0]), int(line.split(',')[1])) for line in lines]
    return red_tiles

def solve1(red_tiles):
    max_area = 0
    n = len(red_tiles)
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height
            if area > max_area:
                max_area = area
    return max_area



def solve2(red_tiles) -> int:
    # Convert to float tuples for Polygon
    coords_tuples = [(float(x), float(y)) for x, y in red_tiles]
    area_full = Polygon(coords_tuples)

    max_area = 0

    # Function to calculate rectangle area
    def calc_area(a, b):
        return (abs(b[0] - a[0]) + 1) * (abs(b[1] - a[1]) + 1)

    # Check all rectangles
    for i in range(len(red_tiles)):
        for j in range(1, len(red_tiles)):
            a, b = red_tiles[i], red_tiles[j]
            rect = Polygon([
                (a[0], b[1]),
                (b[0], b[1]),
                (b[0], a[1]),
                (a[0], a[1])
            ])
            if rect.within(area_full):
                area = calc_area(a, b)
                if area > max_area:
                    max_area = area

    return max_area



if __name__ == "__main__":
    red_tiles = read_input('input')
    print(solve2(red_tiles))
