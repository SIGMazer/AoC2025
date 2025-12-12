
def read_input(file_name: str) -> list[str]:
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def process_rotation(rotation: str) -> int:
    if rotation[0] == 'L':
        return -int(rotation[1:])
    elif rotation[0] == 'R':
        return int(rotation[1:])
    else:
        raise ValueError("Invalid rotation command")


def solve1(input: list[str]) -> int:
    left: int = 50
    result: int = 0
    for rotation in input:
        left += process_rotation(rotation)
        left %= 100 
        if left == 0:
            result += 1
    return result

def solve2(input: list[str]) -> int:
    left: int = 50
    result: int = 0
    for rotation in input:
        steps: int = process_rotation(rotation)
        direction: int = 1 if steps > 0 else -1
        full, partial = divmod(abs(steps), 100)
        result += full
        next_left: int = left + (partial * direction)

        if left != 0: 
            if direction == 1 and next_left >= 100:
                result += 1
            elif direction == -1 and next_left <= 0:
                result += 1

        left = next_left % 100


    return result


if __name__ == "__main__":
    input: list[str]= read_input("input")
    result: int = solve2(input)
    print(f"Result: {result}")
