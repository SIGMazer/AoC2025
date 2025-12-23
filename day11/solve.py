def read_input(file: str) -> dict[str, list[str]]:
    with open(file, 'r') as f:
        lines = f.readlines()
    
    graph = {}
    for line in lines:
        line = line.strip()
        if line:
            device, outputs = line.split(': ')
            graph[device] = outputs.split()
    
    return graph

def count_paths(graph: dict[str, list[str]], start: str, end: str) -> int:
    if start == end:
        return 1
    
    if start not in graph:
        return 0
    
    total = 0
    for neighbor in graph[start]:
        total += count_paths(graph, neighbor, end)
    
    return total

def count_paths_with_required(graph: dict[str, list[str]], start: str, end: str, required: set[str], memo: dict = None) -> int:
    if memo is None:
        memo = {}
    
    required_frozen = frozenset(required)
    
    def dfs(node: str, visited_required: frozenset) -> int:
        if node == end:
            return 1 if visited_required == required_frozen else 0
        
        key = (node, visited_required)
        if key in memo:
            return memo[key]
        
        if node not in graph:
            return 0
        
        new_visited = visited_required | ({node} if node in required else set())
        total = 0
        for neighbor in graph[node]:
            total += dfs(neighbor, new_visited)
        
        memo[key] = total
        return total
    
    return dfs(start, frozenset())

def solve1(graph: dict[str, list[str]]) -> int:
    return count_paths(graph, 'you', 'out')

def solve2(graph: dict[str, list[str]]) -> int:
    return count_paths_with_required(graph, 'svr', 'out', {'dac', 'fft'})

if __name__ == "__main__":
    graph = read_input('input')
    print(solve1(graph))
    print(solve2(graph))
