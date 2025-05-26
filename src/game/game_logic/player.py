# src/game/game_logic/player.py
import pygame
import math
from src.engine.utils.map import Map

class Player:
    """
    Manages the player's position, orientation, and movement within the maze.
    Handles collision detection with maze walls.
    """
    def __init__(self, initial_pos: tuple[float, float], initial_angle: float, 
                 maze: Map, speed: float = 0.05, rotation_speed: float = 0.05,
                 collision_radius: float = 0.2): # Added collision_radius to constructor
        """
        Initializes the Player.

        Args:
            initial_pos (tuple[float, float]): The starting (x, y) coordinates of the player.
            initial_angle (float): The initial viewing angle of the player in radians.
            maze (Map): The Map object representing the game maze.
            speed (float): The movement speed of the player.
            rotation_speed (float): The rotation speed of the player.
            collision_radius (float): The radius used for collision detection around the player.
        """
        self.x, self.y = initial_pos
        self.angle = initial_angle
        self.maze = maze

        self.speed = speed
        self.rotation_speed = rotation_speed
        self.collision_radius = collision_radius # Assigned from constructor

    @property
    def pos(self) -> tuple[float, float]:
        """Returns the current position of the player."""
        return (self.x, self.y)

    def _check_collision(self, new_x: float, new_y: float) -> bool:
        """
        Checks if a new position collides with a wall in the maze.
        Uses a collision radius for better player movement experience.
        """
        # Define corner points relative to the player's new center
        # These points are checked for collision
        corners = [
            (new_x - self.collision_radius, new_y - self.collision_radius),
            (new_x + self.collision_radius, new_y - self.collision_radius),
            (new_x - self.collision_radius, new_y + self.collision_radius),
            (new_x + self.collision_radius, new_y + self.collision_radius)
        ]

        for cx, cy in corners:
            grid_x = int(cx)
            grid_y = int(cy)

            # Check if out of bounds or colliding with a wall (value 1)
            # Ensure grid_y and grid_x are within valid maze dimensions
            if not (0 <= grid_y < self.maze.height and 0 <= grid_x < self.maze.width) or \
               self.maze.grid[grid_y][grid_x] == 1:
                return True # Collision detected

        return False # No collision

    def _move(self, dx: float, dy: float):
        """
        Attempts to move the player by (dx, dy) applying collision detection.
        Performs sliding collision if only one axis collides.
        """
        # Attempt move in X direction first
        new_x = self.x + dx
        if not self._check_collision(new_x, self.y):
            self.x = new_x
        else:
            # If X collides, try moving only Y
            if not self._check_collision(self.x, self.y + dy):
                self.y += dy
            return

        # If X was successful, attempt move in Y direction
        new_y = self.y + dy
        if not self._check_collision(self.x, new_y):
            self.y = new_y

    def update(self):
        """
        Updates the player's position and angle based on keyboard input.
        This method uses pygame.key.get_pressed() for continuous movement.
        """
        keys = pygame.key.get_pressed()

        # Movement (W/S or Up/Down)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dx = self.speed * math.cos(self.angle)
            dy = self.speed * math.sin(self.angle)
            self._move(dx, dy)

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dx = -self.speed * math.cos(self.angle)
            dy = -self.speed * math.sin(self.angle)
            self._move(dx, dy)

        # Rotation (A/D or Left/Right)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle -= self.rotation_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle += self.rotation_speed

        self.angle %= (2 * math.pi)

    def check_end_condition(self, end_point: tuple[int, int]) -> bool:
        """
        Checks if the player has reached the end point of the maze.

        Args:
            end_point (tuple[int, int]): The (x, y) grid coordinates of the maze's end.

        Returns:
            bool: True if player is at or near the end point, False otherwise.
        """
        end_tile_x, end_tile_y = end_point
        # Consider the player to have reached the end if their center is within the end tile
        return int(self.x) == end_tile_x and int(self.y) == end_tile_y