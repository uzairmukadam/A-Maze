# src/game/game_logic/player.py
import math
import pygame
from src.game.constants import Constants

class Player:
    """
    Represents the player character within the maze.
    Handles player position, orientation, movement, collision detection, and maze completion.
    """
    def __init__(self, maze):
        """
        Initializes the Player with maze-specific data and default constants.

        Args:
            maze (dict): A dictionary containing maze details like 'mazeData',
                         'startCoordinate', and 'endCoordinate'.
        """
        self.x, self.y = [0.0, 0.0]
        self.angle = 0.0

        # Store maze properties
        self.maze_data = maze["mazeData"]
        self.maze_start = maze["startCoordinate"]
        self.maze_end = maze["endCoordinate"]

        self.speed = Constants.PLAYER_SPEED
        self.rotation_speed = Constants.PLAYER_ROTATION_SPEED
        self.collision_radius = Constants.PLAYER_COLLISION_RADIUS

        self.get_start_values()

    def get_start_values(self):
        """
        Calculates and sets the player's initial precise position (centered in start cell)
        and orientation based on the maze's start coordinate and surrounding walls.
        """
        start_x_centered = self.maze_start[0] + 0.5
        start_y_centered = self.maze_start[1] + 0.5
        self.x, self.y = [start_x_centered, start_y_centered]

        start_row, start_col = self.maze_start[1], self.maze_start[0]

        if start_row - 1 >= 0 and self.maze_data[start_row - 1][start_col] == 0:
            self.angle = 3 * math.pi / 2
        elif start_col + 1 < len(self.maze_data[0]) and self.maze_data[start_row][start_col + 1] == 0:
            self.angle = 0
        elif start_row + 1 < len(self.maze_data) and self.maze_data[start_row + 1][start_col] == 0:
            self.angle = math.pi / 2
        elif start_col - 1 >= 0 and self.maze_data[start_row][start_col - 1] == 0:
            self.angle = math.pi
        else:
            print(f"[WARNING] Player start at {self.maze_start} is surrounded by walls or invalid path.")
            self.angle = 0

    def check_collision(self, target_x, target_y):
        """
        Checks for collision at a given target (x, y) position using the player's collision radius.
        It checks the four corners of the player's bounding box against maze walls.

        Args:
            target_x (float): The X-coordinate to check.
            target_y (float): The Y-coordinate to check.

        Returns:
            bool: True if a collision with a wall (value 1) is detected, False otherwise.
        """
        corners = [(target_x + self.collision_radius, target_y + self.collision_radius),
                   (target_x + self.collision_radius, target_y - self.collision_radius),
                   (target_x - self.collision_radius, target_y + self.collision_radius),
                   (target_x - self.collision_radius, target_y - self.collision_radius)]
        
        for cx, cy in corners:
            grid_x = int(cx)
            grid_y = int(cy)

            if 0 <= grid_y < len(self.maze_data) and 0 <= grid_x < len(self.maze_data[0]):
                if self.maze_data[grid_y][grid_x] == 1:
                    return True
            else:
                return True
            
        return False

    def move(self, dx, dy):
        """
        Attempts to move the player by (dx, dy) respecting maze collisions.
        This implementation checks X and Y movement independently, allowing for
        sliding along walls if one component of a diagonal move is blocked.

        Args:
            dx (float): Change in X-coordinate.
            dy (float): Change in Y-coordinate.
        """
        potential_x = self.x + dx
        if not self.check_collision(potential_x, self.y):
            self.x = potential_x
        
        potential_y = self.y + dy
        if not self.check_collision(self.x, potential_y):
            self.y = potential_y

    def check_end(self):
        """
        Checks if the player has reached the maze's end coordinate.

        Returns:
            bool: True if the player's current grid cell matches the end coordinate, False otherwise.
        """
        current_grid_x = int(self.x)
        current_grid_y = int(self.y)

        if self.maze_end == [current_grid_x, current_grid_y]:
            return True
        return False

    def update(self):
        """
        Updates the player's state based on user input (keyboard presses).
        Handles movement and rotation.

        Returns:
            str or None: "end" if the player reaches the maze end, otherwise None.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dx = self.speed * math.cos(self.angle)
            dy = self.speed * math.sin(self.angle)
            self.move(dx, dy)

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dx = -self.speed * math.cos(self.angle)
            dy = -self.speed * math.sin(self.angle)
            self.move(dx, dy)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle -= self.rotation_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle += self.rotation_speed

        self.angle %= (2 * math.pi)

        if self.check_end():
            return "end"

        return None
