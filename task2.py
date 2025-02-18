# Step 2: Generate Delivery Points

# This tasks builds on task 1 by generating unique delivery points within the grid. This task also initisialises
# the delivery robot. The robot is given a starting position (user input) and is capable of moving in 4 directions;
# up, down, right, left. It can also deliver parcels when it reaches a delivery point and then update the grid 
# to make it a clear cell. This repeats until all the parcels are delivered, where the robot will then stop and
# alert the user.

# This task demonstrates the robot's ability to autonomosly make decisions and update dynamically in real time.

import random

# Step 1: Define the Robot Class
class SmartDeliveryRobot:
    def __init__(self, grid_size, start_x, start_y, delivery_points):
        self.grid_size = grid_size
        self.x = start_x
        self.y = start_y
        self.delivery_points = set(delivery_points)
        self.delivered_points = set()

    # Move actions
    def move_left(self):
        if self.y > 1:
            self.y -= 1
            print(f"Moved left to ({self.x},{self.y})")
        else:
            print("Cannot move left.")

    def move_right(self):
        if self.y < self.grid_size:
            self.y += 1
            print(f"Moved right to ({self.x},{self.y})")
        else:
            print("Cannot move right.")

    def move_up(self):
        if self.x > 1:
            self.x -= 1
            print(f"Moved up to ({self.x},{self.y})")
        else:
            print("Cannot move up.")

    def move_down(self):
        if self.x < self.grid_size:
            self.x += 1
            print(f"Moved down to ({self.x},{self.y})")
        else:
            print("Cannot move down.")

    # Delivery action
    def deliver(self):
        if (self.x, self.y) in self.delivery_points:
            self.delivered_points.add((self.x, self.y))
            self.delivery_points.remove((self.x, self.y))
            print(f"Delivered at ({self.x},{self.y})")
        else:
            print(f"No delivery at ({self.x},{self.y})")

    # Check if all deliveries are completed
    def all_delivered(self):
        return len(self.delivery_points) == 0

    # Display grid (same format as Task 1)
    def display_grid(self):
        grid = [[f"({x},{y}) Clear" for y in range(1, self.grid_size + 1)] for x in range(1, self.grid_size + 1)]
        
        # Mark delivery points
        for (dx, dy) in self.delivery_points:
            grid[dx - 1][dy - 1] = f"({dx},{dy}) Delivery"
        
        # Mark robot position
        grid[self.x - 1][self.y - 1] = f"({self.x},{self.y}) Robot"
        
        # Print the grid
        for row in grid:
            print(" | ".join(row))
        print()

# Step 2: Get user input for grid size
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

# Step 3: Generate delivery points
def generate_delivery_points(N):
    max_deliveries = (N * N) // 2  # Ensure delivery points are reasonable
    num_deliveries = random.randint(1, max_deliveries)  # Reduce number of deliveries
    delivery_points = set()
    
    while len(delivery_points) < num_deliveries:
        x = random.randint(1, N)
        y = random.randint(1, N)
        delivery_points.add((x, y))
    
    return list(delivery_points)

# Step 4: Get robot's starting position
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

# Main function to run Task 2
def main():
    # Get grid size
    N = get_grid_size()

    # Generate random delivery points
    delivery_points = generate_delivery_points(N)

    # Get starting position
    start_x, start_y = get_starting_position(N)

    # Initialize robot
    robot = SmartDeliveryRobot(N, start_x, start_y, delivery_points)

    # Display initial grid
    print("\nGenerated Environment:")
    robot.display_grid()

    # Simulate some moves
    robot.move_right()
    robot.display_grid()

    robot.move_down()
    robot.display_grid()

    robot.deliver()
    robot.display_grid()

    # Check if all deliveries are complete
    if robot.all_delivered():
        print("\nAll deliveries completed!")
    else:
        print("\nDeliveries remaining:", robot.delivery_points)

# Run the program
if __name__ == "__main__":
    main()
