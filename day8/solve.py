
from collections import defaultdict

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            return False

        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def read_file(file: str) -> list[tuple[int,int,int]]:
    with open(file, 'r') as f:
        lines = f.readlines()
    points = []
    for line in lines:
        parts = line.strip().split(',')
        points.append((int(parts[0]), int(parts[1]), int(parts[2])))
    return points


def calculate_edges(points: list[tuple[int,int,int]]) -> list[tuple[int,int,int]]:
    edges = []
    for i in range(len(points)):
        x1, y1, z1 = points[i]
        for j in range(i + 1, len(points)):
            x2, y2, z2 = points[j]
            d = (
                    (x2 - x1) ** 2 +
                    (y2 - y1) ** 2 +
                    (z2 - z1) ** 2
                )
            edges.append((i, j, d))
    return edges

def solve1(points: list[tuple[int,int,int]],limit: int) -> int:
    edges = calculate_edges(points)
    edges.sort(key=lambda x: x[2])
    uf = UnionFind(len(points))

    attempts = 0
    for i, j, _ in edges:
        if attempts == limit:
            break
        uf.union(i,j)
        attempts +=1
    components = {}
    for i in range(len(points)):
        root = uf.find(i)
        components[root] = uf.size[root]
    sizes = sorted(components.values(), reverse=True)
    return sizes[0] * sizes[1] * sizes[2]

def solve2(points: list[tuple[int,int,int]]) -> int:
    edges = calculate_edges(points)
    edges.sort(key=lambda x: x[2])

    uf = UnionFind(len(points))

    for i, j, _ in edges:
        merged = uf.union(i, j)
        if merged:
            root = uf.find(i)
            if uf.size[root] == len(points):
                x1 = points[i][0]
                x2 = points[j][0]
                return x1 * x2

    return 0

if __name__ == "__main__":
    points = read_file('input')
    print(solve1(points,1000))
    print(solve2(points))
