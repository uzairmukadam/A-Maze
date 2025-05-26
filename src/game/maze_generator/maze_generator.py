# src/game/maze_generator/maze_generator.py
from src.engine.utils.map import Map

class MazeGenerator:
    """
    Base class for all maze generation algorithms.
    Provides common properties and an interface for generating mazes.
    """
    def __init__(self, width: int, height: int, algorithm_name: str, config: dict):
        """
        Initializes the MazeGenerator.

        Args:
            width (int): The desired width of the maze grid.
            height (int): The desired height of the maze grid.
            algorithm_name (str): The name of the maze generation algorithm.
            config (dict): The game configuration dictionary.
        """
        if not (isinstance(width, int) and width > 0 and
                isinstance(height, int) and height > 0):
            raise ValueError("Maze dimensions must be positive integers.")

        self.width = width
        self.height = height
        self.algorithm_name = algorithm_name
        self.config = config # Pass config down for any algorithm-specific settings

        # Initialize maze with all walls (1) by default
        self.maze_grid: list[list[int]] = [[1] * width for _ in range(height)]
        self.start_point: tuple[int, int] = (0, 0)
        self.end_point: tuple[int, int] = (width - 1, height - 1)
        self.name: str = f"{algorithm_name} Maze ({width}x{height})" # Default descriptive name

    def generate_maze(self):
        """
        Abstract method to be implemented by concrete maze generation algorithms.
        This method should populate `self.maze_grid`.
        """
        raise NotImplementedError("Subclasses must implement 'generate_maze' method.")

    def _is_valid_cell(self, x: int, y: int) -> bool:
        """
        Helper method to check if a given coordinate is within the maze bounds.

        Args:
            x (int): The x-coordinate (column).
            y (int): The y-coordinate (row).

        Returns:
            bool: True if the cell is valid, False otherwise.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def set_start(self, x: int, y: int):
        """Sets the starting point of the maze."""
        if not self._is_valid_cell(x, y):
            raise ValueError(f"Start point ({x},{y}) is out of maze bounds.")
        self.start_point = (x, y)

    def set_end(self, x: int, y: int):
        """Sets the ending point of the maze."""
        if not self._is_valid_cell(x, y):
            raise ValueError(f"End point ({x},{y}) is out of maze bounds.")
        self.end_point = (x, y)

    def get_maze(self) -> dict:
        """
        Generates the maze (if not already generated) and returns a dictionary
        containing the maze details, including a Map object.

        Returns:
            dict: A dictionary with maze name, algorithm, Map object, start, and end points.
        """
        self.generate_maze() # Ensure maze is generated before returning
        return {
            "name": self.name,
            "algorithm": self.algorithm_name,
            "maze": Map(self.width, self.height, self.maze_grid), # Create Map object
            "start": self.start_point,
            "end": self.end_point
        }