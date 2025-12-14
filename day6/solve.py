import numpy as np


# @return (list[int][int]), list[str])
def read_input(file: str) -> tuple[list[list[int]], list[str]]:
    with open(file, "r") as f:
        lines = f.read().strip().split("\n")

    operations: list[str] = lines.pop().strip().split()
    data: list[list[int]] = []
    for line in lines:
        data.append([int(x) for x in line.strip().split()])
    return data, operations

def part1(data: list[list[int]], instructions: list[str]) -> int:

    result = 0
    data_array = np.array(data)
    for i, instr in enumerate(instructions):
        if instr == "+":
            result += data_array[:, i].sum()
        else: 
            result += data_array[:, i].prod()
    return result

def read_input_with_padding(file: str) -> tuple[list[str], list[str]]:
    """Read input and return raw lines (without operations) and operations"""
    with open(file, "r") as f:
        lines = f.read().split("\n")
    
    # Remove empty lines from end
    while lines and not lines[-1].strip():
        lines.pop()
    
    # Last line is operations
    operations = lines.pop().strip().split()
    
    return lines, operations




def part2_data_prcessing(lines: list[str]) -> list[list[int]]:
    if not lines:
        return []
    
    max_len = max(len(line) for line in lines)
    padded_lines = [line.ljust(max_len) for line in lines]
    
    is_separator = []
    for col_idx in range(max_len):
        column_chars = [line[col_idx] for line in padded_lines]
        is_separator.append(all(c == ' ' for c in column_chars))
    
    # Group consecutive separators and non-separators
    problems: list[list[int]] = []
    current_problem: list[int] = []
    
    # Read from right to left
    col_idx = max_len - 1
    while col_idx >= 0:
        if is_separator[col_idx]:
            # Skip separator columns
            if current_problem:
                problems.append(current_problem)
                current_problem = []
            col_idx -= 1
        else:
            column_chars = [line[col_idx] for line in padded_lines]
            digits = []
            for c in column_chars:
                if c != ' ':
                    digits.append(c)
            
            if digits:
                number = int(''.join(digits))
                current_problem.append(number)
            col_idx -= 1
    
    if current_problem:
        problems.append(current_problem)
    
    return problems


def part2(problems: list[list[int]], instructions: list[str]) -> int:
    result = 0
    reversed_instructions = instructions[::-1]
    
    for i, (problem_numbers, operation) in enumerate(zip(problems, reversed_instructions)):
        
        if operation == "+":
            problem_result = sum(problem_numbers)
        else:  # multiplication
            problem_result = 1
            for num in problem_numbers:
                problem_result *= num
        
        result += problem_result
    
    return result


if __name__ == "__main__":
    input_file = "input"
    lines, operations = read_input_with_padding(input_file)
    
    problems = part2_data_prcessing(lines)
    result = part2(problems, operations)
    print(result)
    
    # result = part1(data, instructions)
    # print(f"Result: {result}")
