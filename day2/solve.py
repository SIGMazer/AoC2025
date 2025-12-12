
def read_input(file_path: str) -> list[tuple[int, int]]:
    with open(file_path, 'r') as file:
        line: str = file.readline().strip()
        pairs: list[tuple[int, int]] = []
        for part in line.split(','):
            a, b = map(int, part.split('-'))
            pairs.append((a, b))
        return pairs


def find_repeated_seq(s: str) -> bool:
    # find seq like 1111 123123 993993
    n = len(s)
    for length in range(1, n // 2 + 1):
        if n % length == 0:
            seq = s[:length]
            if seq * (n // length) == s:
                return True
    return False

def is_invalid_id(n: int) -> bool:
    s = str(n)

    # must be even-length (otherwise can't be S + S)
    if len(s) % 2 != 0:
        return False

    # no leading zeros allowed
    if s[0] == '0':
        return False

    half = len(s) // 2
    left = s[:half]
    right = s[half:]

    return left == right


def solve(pairs: list[tuple[int, int]], part: int) -> int:
    restult = 0 
    for pair in pairs:
        a, b = pair
        for num in range(a, b + 1):
            s = str(num)
            if part == 1:
                if is_invalid_id(num):
                    restult += num
            else:
                if find_repeated_seq(s):
                    restult += num
    return restult


if __name__ == "__main__":
    input_file = 'input'
    pairs = read_input(input_file)
    result = solve(pairs,1) 
    print(f"Result Part1: {result}")
    result = solve(pairs,2) 
    print(f"Result Part2: {result}")
    
