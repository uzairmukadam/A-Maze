from src.engine.utils.map import Map

class MazeGenerator:
    def __init__(self, width, height, algorithm, name="new map"):
        self.width = width
        self.height = height
        self.algorithm = algorithm
        self.maze = [[1] * width for _ in range(height)]
        self.start = (0, 0)
        self.end = (width - 1, height - 1)
        self.name = name

    def generate_maze(self):
        pass

    def _is_valid_cell(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def set_start(self, x, y):
        self.start = (x, y)

    def set_end(self, x, y):
        self.end = (x, y)

    def get_maze(self):
        self.generate_maze()
        return {"name": self.name, "algorithm": self.algorithm, "maze": Map(self.width, self.height, self.maze), "start": self.start, "end": self.end}
