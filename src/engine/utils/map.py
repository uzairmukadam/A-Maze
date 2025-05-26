class Map:
    def __init__(self, width, height, grid):
        self.width = width
        self.height = height
        self.grid = grid

    def print_grids(self):
        print(f"Map ({self.width}x{self.height}):")
        
        for r in range(self.height):
            for c in range(self.width):
                print(self.grid[r][c], end="")
            print()

if __name__ == "__main__":
    width = 5
    height = 5
    grid = [[0, 1, 1, 1, 1],
            [0, 0, 0, 1, 1],
            [1, 1, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 0, 0]]
    
    map = Map(width, height, grid)

    map.print_grids()