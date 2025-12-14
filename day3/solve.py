
def read_input(file:str) -> list[str]:
    with open(file, 'r') as f:
        return [line.strip() for line in f.readlines()]


# @input nums: str
# @return int the largest possible composed number from two digits in nums in order
def find_largest_jolts(nums: str) -> int:
    largest = -1
    length = len(nums)
    for i in range(length):
        for j in range(i + 1, length):
            composed = int(nums[i] + nums[j])
            if composed > largest:
                largest = composed
    return largest

def find_largest_jolts_part2(nums: str) -> int:
    stack = [] 
    to_remove = len(nums) -12

    for digit in nums:
        while stack and to_remove > 0 and stack[-1] < digit:
            stack.pop()
            to_remove -= 1
        stack.append(digit)
    while to_remove > 0:
        stack.pop()
        to_remove -= 1
    return int(''.join(stack[:12]))



def part1(input: list[str]) -> int:
    total = 0
    for line in input:
        jolts = find_largest_jolts(line)
        total += jolts
    return total

def part2(input: list[str]) -> int:
    total = 0
    for line in input:
        jolts = find_largest_jolts_part2(line)
        total += jolts
    return total


if __name__ == "__main__":
    input_data = read_input('input')
    result = part2(input_data)
    print(result)
