import random


class Map:
    def __init__(self):
        self.map = None
        self.start = None
        self.exit_block = None


    def generate_random_maze(self, width, height):
        # Initialize the maze with walls (1)
        maze = [[1] * width for _ in range(height)]

        # Create the inner space with paths (0)
        for i in range(1, height - 1):
            for j in range(1, width - 1):
                maze[i][j] = 0

        # Randomly add walls inside the maze
        for _ in range((width * height) // 4):  # Adjust the density of walls
            x = random.randint(1, height - 2)
            y = random.randint(1, width - 2)
            maze[x][y] = 1

        # Define start and end points
        start = (1, 1)
        end = (height - 2, width - 2)

        # Ensure start and end points are paths (0)
        maze[start[0]][start[1]] = 0
        maze[end[0]][end[1]] = 0

        return maze, start, end

    def load_map(self):
        width = 20
        height = 20
        random_maze = self.generate_random_maze(width, height)

        self.map = random_maze[0]

        self.start = random_maze[1]

        self.exit_block = random_maze[2]
