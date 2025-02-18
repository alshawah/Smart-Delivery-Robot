# Advanced Component Task 2: Pathfinding and Optimization

# Building on the enhanced environment, Advanced Task 2 focuses on improving the robot’s navigation through the
# implementation of an A* search algorithm. In this task, the robot calculates the optimal path to each delivery
# point by using Manhattan distance as a heuristic and a priority queue (implemented via heapq - a data structure
# where we can access min and max values of the list much easier) to evaluate the best possible route. The 
# algorithm takes into account the obstacles, no-entry zones, and one-way street constraints, ensuring that the
# path chosen is both efficient and viable within the complex urban grid. As the robot follows the computed route,
# the grid is updated dynamically after each move, and the system recalculates if any environmental changes occur. 

# This task showcases the integration of advanced pathfinding techniques into the autonomous delivery system,
# effectively demonstrating the principles of AI in optimizing real-time decision-making and route planning.

import heapq
import random

# --- Helper Functions for A* Search ---

def heuristic(a, b):
    """Return the Manhattan distance between points a and b."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(cell, N, obstacles, no_entry_zones, one_way_streets):
    """
    Return valid neighbor cells for a given cell.
    If the cell is under a one-way constraint, only return the allowed move.
    Skip neighbors that fall into obstacles or no-entry zones.
    """
    (x, y) = cell
    # Default directions: up, down, left, right
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    # Enforce one-way constraint if applicable
    if cell in one_way_streets:
        d = one_way_streets[cell]
        if d == "up":
            directions = [(-1, 0)]
        elif d == "down":
            directions = [(1, 0)]
        elif d == "left":
            directions = [(0, -1)]
        elif d == "right":
            directions = [(0, 1)]
    
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 1 <= nx <= N and 1 <= ny <= N:
            if (nx, ny) not in obstacles and (nx, ny) not in no_entry_zones:
                neighbors.append((nx, ny))
    return neighbors

def a_star_search(start, goal, N, obstacles, no_entry_zones, one_way_streets):
    """
    Perform A* search from start to goal on an N x N grid.
    Returns the optimal path as a list of cells if found, otherwise None.
    """
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current_priority, current = heapq.heappop(frontier)
        if current == goal:
            break

        for next_cell in get_neighbors(current, N, obstacles, no_entry_zones, one_way_streets):
            new_cost = cost_so_far[current] + 1  # assume each move costs 1
            if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                cost_so_far[next_cell] = new_cost
                priority = new_cost + heuristic(goal, next_cell)
                heapq.heappush(frontier, (priority, next_cell))
                came_from[next_cell] = current

    if goal not in came_from:
        return None  # no path found

    # Reconstruct path from goal to start
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

# --- Advanced Robot Class Using A* Search ---

class SmartDeliveryRobotAdvanced:
    def __init__(self, grid_size, start_x, start_y, delivery_points, obstacles, no_entry_zones, one_way_streets):
        self.grid_size = grid_size
        self.x = start_x
        self.y = start_y
        self.delivery_points = set(delivery_points)
        self.obstacles = obstacles
        self.no_entry_zones = no_entry_zones
        self.one_way_streets = one_way_streets
        self.delivered_points = set()

    def display_grid(self):
        """Display the grid with all elements."""
        grid = [[f"({x},{y}) Clear" for y in range(1, self.grid_size + 1)]
                for x in range(1, self.grid_size + 1)]
        for (dx, dy) in self.delivery_points:
            grid[dx - 1][dy - 1] = f"({dx},{dy}) Delivery"
        for (dx, dy) in self.obstacles:
            grid[dx - 1][dy - 1] = f"({dx},{dy}) Obstacle"
        for (dx, dy) in self.no_entry_zones:
            grid[dx - 1][dy - 1] = f"({dx},{dy}) NoEntry"
        for (dx, dy), d in self.one_way_streets.items():
            grid[dx - 1][dy - 1] = f"({dx},{dy}) OneWay:{d}"
        grid[self.x - 1][self.y - 1] = f"({self.x},{self.y}) Robot"
        for row in grid:
            print(" | ".join(row))
        print()

    def move_along_path(self, path):
        """Follow the given path, updating the robot's position and displaying the grid."""
        for cell in path[1:]:
            self.x, self.y = cell
            print(f"Moved to ({self.x},{self.y})")
            self.display_grid()

    def deliver(self):
        """Perform delivery if the robot is at a delivery point."""
        if (self.x, self.y) in self.delivery_points:
            self.delivery_points.remove((self.x, self.y))
            self.delivered_points.add((self.x, self.y))
            print(f"Delivered at ({self.x},{self.y})")
            self.display_grid()
        else:
            print(f"No delivery at ({self.x},{self.y})")

    def navigate_to_target(self, target):
        """Calculate the optimal path to the target using A* and move along it."""
        path = a_star_search(
            (self.x, self.y), target, self.grid_size,
            self.obstacles, self.no_entry_zones, self.one_way_streets
        )
        if path is None:
            print(f"No available path to {target}.")
        else:
            print(f"Path to {target}: {path}")
            self.move_along_path(path)
            self.deliver()

    def run(self):
        """Autonomously navigate to deliver all parcels."""
        while self.delivery_points:
            # Select the nearest delivery point using Manhattan distance
            target = min(self.delivery_points, key=lambda p: heuristic((self.x, self.y), p))
            self.navigate_to_target(target)
        print("All deliveries completed!")

# --- Environment and Robot Setup Functions ---

def get_grid_size():
    while True:
        try:
            N = int(input("Enter grid size (N x N, where N is between 1 and 6): "))
            if 1 <= N <= 6:
                return N
            else:
                print("Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def generate_delivery_points(N):
    max_deliveries = (N * N) // 2
    num_deliveries = random.randint(1, max_deliveries)
    points = set()
    while len(points) < num_deliveries:
        points.add((random.randint(1, N), random.randint(1, N)))
    return list(points)

def generate_obstacles(N, reserved):
    num_obstacles = random.randint(1, (N * N) // 4)
    obstacles = set()
    while len(obstacles) < num_obstacles:
        cell = (random.randint(1, N), random.randint(1, N))
        if cell not in reserved:
            obstacles.add(cell)
    return obstacles

def generate_no_entry_zones(N, reserved):
    num_zones = random.randint(1, (N * N) // 4)
    zones = set()
    while len(zones) < num_zones:
        cell = (random.randint(1, N), random.randint(1, N))
        if cell not in reserved:
            zones.add(cell)
    return zones

def generate_one_way_streets(N, reserved):
    num_one_way = random.randint(1, (N * N) // 4)
    one_way = {}
    directions = ["up", "down", "left", "right"]
    while len(one_way) < num_one_way:
        cell = (random.randint(1, N), random.randint(1, N))
        if cell not in reserved and cell not in one_way:
            one_way[cell] = random.choice(directions)
    return one_way

def get_starting_position(N):
    while True:
        try:
            x, y = map(int, input("Enter robot starting position (x y): ").split())
            if 1 <= x <= N and 1 <= y <= N:
                return x, y
            else:
                print(f"Enter values between 1 and {N}.")
        except ValueError:
            print("Invalid input. Please enter two integers separated by a space.")

def main():
    N = get_grid_size()
    delivery_points = generate_delivery_points(N)
    reserved = set(delivery_points)
    obstacles = generate_obstacles(N, reserved)
    reserved = reserved.union(obstacles)
    no_entry_zones = generate_no_entry_zones(N, reserved)
    reserved = reserved.union(no_entry_zones)
    one_way_streets = generate_one_way_streets(N, reserved)
    start_x, start_y = get_starting_position(N)
    
    print("\nAdvanced Environment:")
    # Simple grid view for advanced environment
    for x in range(1, N+1):
        row = []
        for y in range(1, N+1):
            cell = f"({x},{y})"
            if (x, y) in delivery_points:
                cell += " Delivery"
            elif (x, y) in obstacles:
                cell += " Obstacle"
            elif (x, y) in no_entry_zones:
                cell += " NoEntry"
            elif (x, y) in one_way_streets:
                cell += f" OneWay:{one_way_streets[(x,y)]}"
            else:
                cell += " Clear"
            row.append(cell)
        print(" | ".join(row))
    print()

    # Initialize and run the advanced robot
    robot = SmartDeliveryRobotAdvanced(N, start_x, start_y, delivery_points, obstacles, no_entry_zones, one_way_streets)
    robot.display_grid()
    robot.run()

if __name__ == "__main__":
    main()
