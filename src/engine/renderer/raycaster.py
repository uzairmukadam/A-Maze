# src/engine/renderer/raycaster.py
import pygame
import math
from src.engine.utils.map import Map 

class Raycaster:
    """
    Renders the 3D perspective of the maze using raycasting.
    """
    def __init__(self, window: pygame.Surface, maze: Map, config: dict, 
                 start_coords: tuple[int, int], end_coords: tuple[int, int]): # <-- NEW ARGS
        """
        Initializes the Raycaster.

        Args:
            window (pygame.Surface): The Pygame surface to draw on.
            maze (Map): The Map object representing the maze grid.
            config (dict): The game configuration, including FOV, resolution, scale.
            start_coords (tuple[int, int]): The (x, y) grid coordinates of the maze start.
            end_coords (tuple[int, int]): The (x, y) grid coordinates of the maze end.
        """
        self.window = window
        self.maze = maze
        self.config = config

        self.fov = math.radians(self.config.get("fov", 75)) 
        self.half_fov = self.fov / 2
        self.scale = self.config.get("scale", 1.0) 
        
        self.resolution_width, self.resolution_height = self.config["resolution"]
        self.num_rays = int(self.resolution_width / self.scale)
        self.delta_angle = self.fov / self.num_rays

        self.start_coords = start_coords # Store start coords
        self.end_coords = end_coords     # Store end coords

        # Define wall colors (simple for now)
        self.wall_colors = {
            'N': (180, 0, 0), # Slightly darker reds/greens/blues
            'S': (0, 180, 0),
            'E': (0, 0, 180),
            'W': (180, 180, 0),
            'default': (120, 120, 120) 
        }
        self.floor_color = (50, 50, 50)
        self.ceiling_color = (80, 80, 80)

        # Colors for start/end points
        self.start_wall_color = (0, 255, 0) # Bright Green
        self.end_wall_color = (255, 0, 0)   # Bright Red


    def _raycast(self, player_pos: tuple[float, float], ray_angle: float) -> tuple[float, str, int, int]: # <-- UPDATED RETURN TYPE
        """
        Casts a single ray from the player's position in a given direction
        and returns the distance to the nearest wall, wall's orientation, and hit coordinates.

        Args:
            player_pos (tuple[float, float]): Player's (x, y) coordinates.
            ray_angle (float): Angle of the ray in radians.

        Returns:
            tuple[float, str, int, int]: (Distance to wall, wall orientation, hit_map_x, hit_map_y).
        """
        px, py = player_pos
        
        cos_a = math.cos(ray_angle)
        sin_a = math.sin(ray_angle)

        map_x, map_y = int(px), int(py)

        delta_dist_x = abs(1 / cos_a) if cos_a != 0 else float('inf')
        delta_dist_y = abs(1 / sin_a) if sin_a != 0 else float('inf')

        if cos_a < 0:
            step_x = -1
            side_dist_x = (px - map_x) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_x + 1.0 - px) * delta_dist_x

        if sin_a < 0:
            step_y = -1
            side_dist_y = (py - map_y) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_y + 1.0 - py) * delta_dist_y
        
        hit = False
        side = None 

        while not hit:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0 
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1 

            # Check if ray has hit a wall or start/end point (any non-zero value)
            if 0 <= map_y < self.maze.height and 0 <= map_x < self.maze.width and \
               self.maze.grid[map_y][map_x] != 0: # Check for any wall type
                hit = True

        # Calculate distance to wall
        if side == 0: 
            perp_wall_dist = (map_x - px + (1 - step_x) / 2) / cos_a
            if step_x > 0: wall_orientation = 'E'
            else: wall_orientation = 'W'
        else:
            perp_wall_dist = (map_y - py + (1 - step_y) / 2) / sin_a
            if step_y > 0: wall_orientation = 'S'
            else: wall_orientation = 'N'
        
        if abs(perp_wall_dist) < 0.001:
            perp_wall_dist = 0.001

        return perp_wall_dist, wall_orientation, map_x, map_y # <-- NEW RETURN VALUES

    def render(self, player_pos: tuple[float, float], player_angle: float):
        """
        Renders the 3D view of the maze from the player's perspective.

        Args:
            player_pos (tuple[float, float]): Player's (x, y) coordinates.
            player_angle (float): Player's current viewing angle in radians.
        """
        self.window.fill(self.ceiling_color) # Fill with ceiling color first
        pygame.draw.rect(self.window, self.floor_color, (0, self.resolution_height // 2, self.resolution_width, self.resolution_height // 2))

        start_ray_angle = player_angle - self.half_fov

        for ray_num in range(self.num_rays):
            ray_angle = start_ray_angle + ray_num * self.delta_angle

            # Get new return values from _raycast
            corrected_dist, wall_orientation, hit_x, hit_y = self._raycast(player_pos, ray_angle) 
            
            actual_ray_angle = ray_angle - player_angle
            corrected_dist *= math.cos(actual_ray_angle)

            wall_height = int(self.resolution_height / (corrected_dist + 0.001)) * self.scale

            wall_top = (self.resolution_height // 2) - (wall_height // 2)
            # wall_bottom = (self.resolution_height // 2) + (wall_height // 2) # Not strictly needed if using rect

            # --- Determine Wall Color (including start/end points) ---
            current_wall_color = None
            if (hit_x, hit_y) == self.start_coords:
                current_wall_color = self.start_wall_color
            elif (hit_x, hit_y) == self.end_coords:
                current_wall_color = self.end_wall_color
            else:
                current_wall_color = self.wall_colors.get(wall_orientation, self.wall_colors['default'])
            
            # Simple distance shading
            max_shading_dist = self.config.get("draw_distance", 5) 
            shading_factor = 1 - min(1, corrected_dist / max_shading_dist)
            
            shaded_color = (
                int(current_wall_color[0] * shading_factor),
                int(current_wall_color[1] * shading_factor),
                int(current_wall_color[2] * shading_factor)
            )

            column_x = int(ray_num * self.scale)

            pygame.draw.rect(self.window, shaded_color, 
                             (column_x, wall_top, int(self.scale), wall_height))