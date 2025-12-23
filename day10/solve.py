import re
from itertools import product
from z3 import Int, Solver, sat

def read_input(file: str) -> list[tuple[list[int], list[list[int]], list[int]]]:
    with open(file, 'r') as f:
        lines = f.readlines()
    
    machines = []
    for line in lines:
        line = line.strip()
        if line:
            indicator_match = re.search(r'\[([.#]+)\]', line)
            indicator = indicator_match.group(1)
            target_lights = [1 if c == '#' else 0 for c in indicator]
            
            button_matches = re.findall(r'\(([0-9,]+)\)', line)
            buttons = []
            for match in button_matches:
                if match:
                    buttons.append([int(x) for x in match.split(',')])
            
            joltage_match = re.search(r'\{([0-9,]+)\}', line)
            target_joltage = [int(x) for x in joltage_match.group(1).split(',')]
            
            machines.append((target_lights, buttons, target_joltage))
    
    return machines

def solve_machine(target, buttons):
    n_lights = len(target)
    n_buttons = len(buttons)
    
    matrix = []
    for light_idx in range(n_lights):
        row = [1 if light_idx in button else 0 for button in buttons]
        matrix.append(row + [target[light_idx]])
    
    pivot_cols = []
    pivot_row = 0
    
    for col in range(n_buttons):
        found = False
        for row in range(pivot_row, n_lights):
            if matrix[row][col] == 1:
                matrix[pivot_row], matrix[row] = matrix[row], matrix[pivot_row]
                found = True
                break
        
        if not found:
            continue
        
        pivot_cols.append(col)
        
        for row in range(n_lights):
            if row != pivot_row and matrix[row][col] == 1:
                for c in range(n_buttons + 1):
                    matrix[row][c] ^= matrix[pivot_row][c]
        
        pivot_row += 1
    
    for row in range(pivot_row, n_lights):
        if matrix[row][-1] == 1:
            return None
    
    free_vars = [i for i in range(n_buttons) if i not in pivot_cols]
    
    particular = [0] * n_buttons
    for i, col in enumerate(pivot_cols):
        particular[col] = matrix[i][-1]
    
    if not free_vars:
        return sum(particular)
    
    min_presses = sum(particular)
    
    for combo in product([0, 1], repeat=len(free_vars)):
        solution = particular[:]
        for i, var_idx in enumerate(free_vars):
            solution[var_idx] = combo[i]
        
        for i in range(len(pivot_cols) - 1, -1, -1):
            col = pivot_cols[i]
            val = matrix[i][-1]
            for j in range(col + 1, n_buttons):
                if matrix[i][j] == 1:
                    val ^= solution[j]
            solution[col] = val
        
        state = [0] * n_lights
        for button_idx, presses in enumerate(solution):
            if presses:
                for light in buttons[button_idx]:
                    if light < n_lights:
                        state[light] ^= 1
        
        if state == target:
            min_presses = min(min_presses, sum(solution))
    
    return min_presses

def solve_joltage(target, buttons):
    n_counters = len(target)
    n_buttons = len(buttons)
    
    button_vars = [Int(f'b{i}') for i in range(n_buttons)]
    s = Solver()
    
    for counter_idx, joltage_req in enumerate(target):
        s.add(joltage_req == sum([button_vars[j] for j in range(n_buttons) if counter_idx in buttons[j]]))
    
    for button_var in button_vars:
        s.add(button_var >= 0)
    
    for i in range(max(target), max(target) + 1000):
        s.push()
        s.add(sum(button_vars) == i)
        if s.check() == sat:
            s.pop()
            return i
        s.pop()
    
    return None

def solve1(input: list[tuple[list[int], list[list[int]], list[int]]]) -> int:
    total = 0
    for target_lights, buttons, _ in input:
        presses = solve_machine(target_lights, buttons)
        if presses is not None:
            total += presses
    return total

def solve2(input: list[tuple[list[int], list[list[int]], list[int]]]) -> int:
    total = 0
    for _, buttons, target_joltage in input:
        presses = solve_joltage(target_joltage, buttons)
        if presses is not None:
            total += presses
    return total

if __name__ == "__main__":
    input = read_input('input')
    print(solve1(input))
    print(solve2(input))
