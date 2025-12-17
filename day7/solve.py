from collections import defaultdict

def read_input(file: str) -> list[str]:
    with open(file, 'r') as f:
        return f.read().strip().splitlines()



def solve1(map: list[str]) -> int:
    result: int = 0
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 'S':
                if i+1 < len(map):
                    map[i+1] = map[i+1][:j] + '|' + map[i+1][j+1:]
            elif map[i][j] == '^':
                if map[i-1][j] == '|':
                    row = list(map[i])
                    row[j+1] = '|'
                    row[j-1] = '|'
                    map[i] = "".join(row)
                    result += 1
            elif map[i-1][j] == '|':
                row = list(map[i])
                row[j] = '|'
                map[i] = "".join(row)
    return result



def solve2(map: list[str]) -> int:
    map_new = [list(row) for row in map]
    rows = len(map_new)
    cols = len(map_new[0])

    #find S
    for i in range(rows):
        for j in range(cols):
            if map_new[i][j] == 'S':
                start = (i, j)
    dp = defaultdict(int)
    dp[start] = 1
    for i in range(start[0], rows):
        for j in range(cols):
            if map_new[i][j] == 'S':
                continue
            if map_new[i][j] == '^':
                if i > 0 and dp[(i-1, j)] > 0:
                    dp[(i, j+1)] += dp[(i-1, j)]
                    dp[(i, j-1)] += dp[(i-1, j)]
            else:
                dp[(i, j)] += dp[(i-1, j)]
    result = 0
    for j in range(cols):
        result += dp[(rows-1, j)]
    return result



if __name__ == "__main__":

    map = read_input('input')
    print(solve2(map))

