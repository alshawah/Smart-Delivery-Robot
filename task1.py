# task 1: Define the Grid Size

# In this inital task, the user is prompted to enter the size of the grid they want (N,N), which can 
# only be a number from 1-6. The program will then randomly generate a set of delivery points on the 
# grid that the user defined.  Each cell will be labeled as either 'clear' or 'delivery'. The purpose
# of this task was to create the basic environment that the final Robot will operate in, and ensuring
# that the inputs by the user are all validated.

import random

# Step 1: Define the Grid Size
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

# Step 2: Generate Delivery Points
def generate_delivery_points(N, num_deliveries):
    delivery_points = []
    while len(delivery_points) < num_deliveries:
        x = random.randint(1, N)
        y = random.randint(1, N)
        if (x, y) not in delivery_points:
            delivery_points.append((x, y))
    return delivery_points

# Step 3: Display the Grid
def display_grid(N, delivery_points):
    grid = [[f"({x},{y}) Clear" for y in range(1, N + 1)] for x in range(1, N + 1)]
    for (x, y) in delivery_points:
        grid[x - 1][y - 1] = f"({x},{y}) Delivery"
    for row in grid:
        print(" | ".join(row))

# Main function to run Task 1
def main():
    # Step 1: Get grid size from user
    N = get_grid_size()
    
    # Step 2: Generate delivery points
    num_deliveries = random.randint(1, N * N)  # Random number of deliveries
    delivery_points = generate_delivery_points(N, num_deliveries)
    
    # Step 3: Display the grid
    print("\nGenerated Environment:")
    display_grid(N, delivery_points)

# Run the program
if __name__ == "__main__":
    main()
