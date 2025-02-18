# Task 3: Run the Agent

# In This task, the final task before the Advanced category, we build on both tasks 1 and 2 to create a robot
# that continuously select the nearest delivery point and move step-by-step towards it, calculating the fastest 
# way to arrive there. As the robot progresses, the grid updates after each move to show the current position 
# to the user. Every time the robot delivers a parcel, up until the robot reaches the final parcel, the program
# will update us by displaying the grid to the user. 

# In order to calculate the fastest path to the delivery cell, the roboy uses the Manhattan distance as a 
# heuristic to find out which delivery point is the closest. It then moves one cell at a time in the optimal 
# direction.

# Task 3 bings together all components of the program by demonstrating validation, grid visualisation, and proximity
# based navigation are integreated to create an autonomous deliver system - a very very simple AI.

import random

# Step 1: Define the Smart Delivery Robot Class
class SmartDeliveryRobot:
    def __init__(self, grid_size, start_x, start_y, delivery_points):
        self.grid_size = grid_size
        self.x = start_x
        self.y = start_y
        self.delivery_points = set(delivery_points)
        self.delivered_points = set()

    # General move function: dx, dy are the changes in x and y directions.
    def move(self, dx, dy):
        new_x, new_y = self.x + dx, self.y + dy
        if 1 <= new_x <= self.grid_size and 1 <= new_y <= self.grid_size:
            self.x, self.y = new_x, new_y
            print(f"Moved to ({self.x},{self.y})")
        else:
            print("Invalid move. Staying in place.")

    # Delivery action: deliver at the current location if it's a delivery point.
    def deliver(self):
        if (self.x, self.y) in self.delivery_points:
            self.delivered_points.add((self.x, self.y))
            self.delivery_points.remove((self.x, self.y))
            print(f"Delivered at ({self.x},{self.y})")
        else:
            print(f"No delivery at ({self.x},{self.y})")

    # Check if all deliveries have been completed.
    def all_delivered(self):
        return len(self.delivery_points) == 0

    # Display grid (consistent with Task 1 and Task 2)
    def display_grid(self):
        grid = [[f"({x},{y}) Clear" for y in range(1, self.grid_size + 1)]
                for x in range(1, self.grid_size + 1)]
        
        # Mark remaining delivery points.
        for (dx, dy) in self.delivery_points:
            grid[dx - 1][dy - 1] = f"({dx},{dy}) Delivery"
        
        # Mark the robot's current position.
        grid[self.x - 1][self.y - 1] = f"({self.x},{self.y}) Robot"
        
        for row in grid:
            print(" | ".join(row))
        print()

    # Autonomous navigation: move toward the nearest delivery point and deliver.
    def navigate_and_deliver(self):
        while not self.all_delivered():
            # If there are remaining deliveries, choose the nearest based on Manhattan distance.
            if self.delivery_points:
                target = min(self.delivery_points, key=lambda p: abs(p[0] - self.x) + abs(p[1] - self.y))
                target_x, target_y = target

                # Determine the next move: prioritize vertical movement, then horizontal.
                if self.x < target_x:
                    self.move(1, 0)  # Move down
                elif self.x > target_x:
                    self.move(-1, 0)  # Move up
                elif self.y < target_y:
                    self.move(0, 1)  # Move right
                elif self.y > target_y:
                    self.move(0, -1)  # Move left

                self.display_grid()

                # If the robot has reached the target delivery point, deliver the parcel.
                if (self.x, self.y) == target:
                    self.deliver()
                    self.display_grid()

        print("All deliveries completed!")

# Helper: Get grid size from the user (as in Task 1)
def get_grid_size():
    while True:
        try:
            N = int(input("Enter the grid size (N x N, where N is between 1 and 6): "))
            if 1 <= N <= 6:
                return N
            else:
                print("Invalid input. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

# Helper: Generate delivery points (limiting to roughly half the grid cells as in Task 2)
def generate_delivery_points(N):
    max_deliveries = (N * N) // 2  # Limit to roughly half the grid cells.
    num_deliveries = random.randint(1, max_deliveries)
    delivery_points = set()
    while len(delivery_points) < num_deliveries:
        x = random.randint(1, N)
        y = random.randint(1, N)
        delivery_points.add((x, y))
    return list(delivery_points)

# Helper: Get the robot's starting position with validation (as in Task 2)
def get_starting_position(N):
    while True:
        try:
            x, y = map(int, input("Enter the robot's starting position (x y): ").split())
            if 1 <= x <= N and 1 <= y <= N:
                return x, y
            else:
                print(f"Invalid position. Enter values between 1 and {N}.")
        except ValueError:
            print("Invalid input. Enter two integers separated by a space.")

# Main function to run Task 3
def main():
    # Get grid size from the user.
    N = get_grid_size()

    # Generate delivery points.
    delivery_points = generate_delivery_points(N)

    # Get the robot's starting position.
    start_x, start_y = get_starting_position(N)

    # Initialize the robot with grid size, starting position, and delivery points.
    robot = SmartDeliveryRobot(N, start_x, start_y, delivery_points)

    # Display the initial grid environment.
    print("\nGenerated Environment:")
    robot.display_grid()

    # Let the robot autonomously navigate and complete deliveries.
    robot.navigate_and_deliver()

# Run the program
if __name__ == "__main__":
    main()
