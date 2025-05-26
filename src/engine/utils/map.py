# src/engine/utils/map.py
class Map:
    """
    Represents the maze map structure, including its dimensions and grid data.
    '0' typically represents a path, '1' represents a wall.
    """
    def __init__(self, width: int, height: int, grid: list[list[int]]):
        """
        Initializes a Map object.

        Args:
            width (int): The width of the maze grid.
            height (int): The height of the maze grid.
            grid (list[list[int]]): A 2D list representing the maze layout.
        """
        if not (isinstance(width, int) and width > 0 and
                isinstance(height, int) and height > 0):
            raise ValueError("Map dimensions must be positive integers.")
        
        if not (isinstance(grid, list) and all(isinstance(row, list) for row in grid)):
            raise TypeError("Grid must be a list of lists.")
        
        if len(grid) != height or any(len(row) != width for row in grid):
            raise ValueError("Grid dimensions do not match specified width and height.")

        self.width = width
        self.height = height
        self.grid = grid

    def print_grids(self):
        """
        Prints a text-based representation of the map grid to the console.
        """
        print(f"Map ({self.width}x{self.height}):")
        
        for r in range(self.height):
            for c in range(self.width):
                print(self.grid[r][c], end="")
            print()

# Example usage (moved to a test file or direct import in generators)
if __name__ == "__main__":
    test_width = 5
    test_height = 5
    test_grid = [[0, 1, 1, 1, 1],
                 [0, 0, 0, 1, 1],
                 [1, 1, 0, 1, 1],
                 [1, 0, 0, 0, 1],
                 [1, 1, 1, 0, 0]]
    
    try:
        test_map = Map(test_width, test_height, test_grid)
        test_map.print_grids()

        # Test invalid dimensions
        # invalid_map = Map(0, 5, test_grid) 
    except ValueError as e:
        print(f"Error creating map: {e}")