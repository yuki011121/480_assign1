import sys
import heapq

def parse_world(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    cols = int(lines[0].strip())  
    rows = int(lines[1].strip())  

    grid = [line.strip() for line in lines[2:]]

    robot_start = None
    dirty_cells = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':  
                robot_start = (r, c)
            elif grid[r][c] == '*':  
                dirty_cells.append((r, c))

    return grid, robot_start, dirty_cells

def generate_successors(state, grid):
    (row, col), dirty_cells = state
    rows = len(grid)
    cols = len(grid[0])
    successors = []

    moves = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    for action, (dr, dc) in moves.items():
        new_row, new_col = row + dr, col + dc

        if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col] != '#':
            new_state = ((new_row, new_col), dirty_cells)
            successors.append((new_state, action))

    if (row, col) in dirty_cells:
        new_dirty_cells = set(dirty_cells)
        new_dirty_cells.remove((row, col))
        new_state = ((row, col), frozenset(new_dirty_cells)) 
        successors.append((new_state, 'V'))

    return successors

def depth_first_search(grid, robot_start, dirty_cells):
    start_state = (robot_start, frozenset(dirty_cells))
    frontier = [(start_state, [])]  

    visited = set() 
    nodes_generated = 1
    nodes_expanded = 0

    while frontier:
        current_state, path = frontier.pop()  # LIFO

        if current_state in visited:
            continue

        nodes_expanded += 1
        visited.add(current_state)

        (pos, dirt) = current_state
        if not dirt: 
            return path, nodes_generated, nodes_expanded

        successors = generate_successors(current_state, grid)
        nodes_generated += len(successors)

        for new_state, action in reversed(successors):
            if new_state not in visited:
                new_path = path + [action]
                frontier.append((new_state, new_path))

    return None, nodes_generated, nodes_expanded

def uniform_cost_search(grid, robot_start, dirty_cells):
    start_state = (robot_start, frozenset(dirty_cells))
    frontier = [(0, start_state, [])] 
    heapq.heapify(frontier)

    visited = set()
    nodes_generated = 1
    nodes_expanded = 0

    while frontier:
        cost, current_state, path = heapq.heappop(frontier) 

        if current_state in visited:
            continue

        nodes_expanded += 1
        visited.add(current_state)

        (pos, dirt) = current_state
        if not dirt: 
            return path, nodes_generated, nodes_expanded

        successors = generate_successors(current_state, grid)
        nodes_generated += len(successors)

        for new_state, action in successors:
            if new_state not in visited:
                new_cost = cost + 1
                new_path = path + [action]
                heapq.heappush(frontier, (new_cost, new_state, new_path))

    return None, nodes_generated, nodes_expanded

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py [algorithm] [world-file]")
        sys.exit(1)

    algorithm = sys.argv[1].lower()
    world_file = sys.argv[2]

    try:
        grid, robot_start, dirty_cells = parse_world(world_file)
    except FileNotFoundError:
        print(f"Error: World file not found at '{world_file}'")
        sys.exit(1)

    if robot_start is None:
        print("Error: No robot start position '@' found in the world file.")
        sys.exit(1)

    if algorithm == "uniform-cost":
        path, generated, expanded = uniform_cost_search(grid, robot_start, dirty_cells)
    elif algorithm == "depth-first":
        path, generated, expanded = depth_first_search(grid, robot_start, dirty_cells)
    else:
        print("Invalid algorithm. Choose 'uniform-cost' or 'depth-first'.")
        sys.exit(1)

    if path is not None:
        for action in path:
            print(action)  
    else:
        print("No solution found.")

    print(f"{generated} nodes generated") 
    print(f"{expanded} nodes expanded")  

if __name__ == "__main__":
    main()
