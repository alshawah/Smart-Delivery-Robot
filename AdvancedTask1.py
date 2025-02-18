# Advanced Component Task 1: Enhanced Environment

# In this task, we extend the basic grid environment by incorporating realistic urban challenges. The program now
# not only generates delivery points but also randomly places obstacles, no-entry zones, and one-way streets 
# within the grid. Each cell is clearly labeled so that users can distinguish between clear cells, delivery points,
# obstacles, and constrained areas such as no-entry zones and one-way streets. The purpose of this enhancement is
# to simulate a more complex urban environment that the Smart Delivery Robot will need to navigate, providing a
# more realistic context for testing its decision-making and adaptability. 

# This task demonstrates the integration of additional environmental constraints, ensuring that the robot's
# navigation system can be further challenged and refined.

import random

# --- Helper Functions ---

def get_grid_size():
    """Prompt the user to enter a grid size (N x N) where 1 <= N <= 6."""
    while True:
        try:
            N = int(input("Enter grid size (N x N, where N is between 1 and 6): "))
            if 1 <= N <= 6:
                return N
            else:
                print("Invalid input. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def generate_delivery_points(N, num_deliveries):
    """Generate a set of delivery points on the grid."""
    delivery_points = set()
    while len(delivery_points) < num_deliveries:
        x = random.randint(1, N)
        y = random.randint(1, N)
        delivery_points.add((x, y))
    return list(delivery_points)

def generate_obstacles(N, num_obstacles, reserved_cells):
    """Generate obstacles on the grid, avoiding reserved cells."""
    obstacles = set()
    while len(obstacles) < num_obstacles:
        x = random.randint(1, N)
        y = random.randint(1, N)
        if (x, y) not in reserved_cells:
            obstacles.add((x, y))
    return obstacles

def generate_no_entry_zones(N, num_zones, reserved_cells):
    """Generate no-entry zones, avoiding reserved cells."""
    zones = set()
    while len(zones) < num_zones:
        x = random.randint(1, N)
        y = random.randint(1, N)
        if (x, y) not in reserved_cells:
            zones.add((x, y))
    return zones

def generate_one_way_streets(N, num_streets, reserved_cells):
    """Generate one-way streets as a dict mapping coordinates to an allowed direction."""
    directions = ['up', 'down', 'left', 'right']
    one_way = {}
    while len(one_way) < num_streets:
        x = random.randint(1, N)
        y = random.randint(1, N)
        if (x, y) not in reserved_cells and (x, y) not in one_way:
            one_way[(x, y)] = random.choice(directions)
    return one_way

def display_advanced_grid(N, delivery_points, obstacles, no_entry_zones, one_way_streets):
    """Display the grid with delivery points, obstacles, no-entry zones, and one-way streets."""
    grid = []
    for x in range(1, N + 1):
        row = []
        for y in range(1, N + 1):
            cell = f"({x},{y})"
            if (x, y) in delivery_points:
                cell += " Delivery"
            elif (x, y) in obstacles:
                cell += " Obstacle"
            elif (x, y) in no_entry_zones:
                cell += " No-Entry"
            elif (x, y) in one_way_streets:
                cell += f" OneWay:{one_way_streets[(x, y)]}"
            else:
                cell += " Clear"
            row.append(cell)
        grid.append(" | ".join(row))
    
    for row in grid:
        print(row)
    print()

# --- Main Advanced Environment Generation ---

def main():
    # Get grid size
    N = get_grid_size()

    # Generate delivery points (limiting to roughly half the grid cells)
    num_deliveries = random.randint(1, (N * N) // 2)
    delivery_points = generate_delivery_points(N, num_deliveries)
    
    # 'Reserved cells' to avoid overlapping elements (delivery points take priority)
    reserved_cells = set(delivery_points)
    
    # Generate obstacles (e.g., up to a quarter of grid cells)
    num_obstacles = random.randint(1, (N * N) // 4)
    obstacles = generate_obstacles(N, num_obstacles, reserved_cells)
    reserved_cells = reserved_cells.union(obstacles)
    
    # Generate no-entry zones (similarly up to a quarter of grid cells)
    num_zones = random.randint(1, (N * N) // 4)
    no_entry_zones = generate_no_entry_zones(N, num_zones, reserved_cells)
    reserved_cells = reserved_cells.union(no_entry_zones)
    
    # Generate one-way streets (as a quarter of grid cells at most)
    num_one_way = random.randint(1, (N * N) // 4)
    one_way_streets = generate_one_way_streets(N, num_one_way, reserved_cells)
    
    # Display the advanced environment grid
    print("\nAdvanced Environment:")
    display_advanced_grid(N, delivery_points, obstacles, no_entry_zones, one_way_streets)

if __name__ == "__main__":
    main()
