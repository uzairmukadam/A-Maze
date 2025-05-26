# src/game/game_logic/game_logic.py
import pygame
import math
from src.engine.utils.map import Map
from src.game.utils.game_constants import GameConstants
from src.engine.renderer.raycaster import Raycaster

from src.game.game_logic.player import Player

class GameLogic:
    """
    Manages the core gameplay mechanics, including player movement,
    collision detection, and interaction with the maze.
    This class will also orchestrate the rendering using a separate renderer.
    """
    def __init__(self, window: pygame.Surface, maze_data: dict, config: dict):
        """
        Initializes the GameLogic.

        Args:
            window (pygame.Surface): The Pygame surface to draw on.
            maze_data (dict): A dictionary containing maze details, including
                              "maze" (Map object), "start" (tuple), "end" (tuple).
            config (dict): The game configuration dictionary (for user-modifiable settings).
        """
        self.window = window
        self.config = config 
        self.maze_data = maze_data
        self.maze: Map = maze_data["maze"]

        self.start_coords: tuple[int, int] = maze_data["start"]
        self.end_coords: tuple[int, int] = maze_data["end"]

        start_x, start_y = self.start_coords
        initial_pos = (start_x + 0.5, start_y + 0.5) 
        initial_angle = self._get_start_angle()

        player_speed = GameConstants.PLAYER_SPEED
        player_rotation_speed = GameConstants.PLAYER_ROTATION_SPEED
        player_collision_radius = GameConstants.PLAYER_COLLISION_RADIUS

        self.player = Player(
            initial_pos, 
            initial_angle, 
            self.maze, 
            speed=player_speed, 
            rotation_speed=player_rotation_speed,
            collision_radius=player_collision_radius
        )
        
        self.draw_distance = self.config["draw_distance"] 

        self.tile_size = 10 
        self._minimap_surface = self._pre_render_minimap() # Pre-render minimap once

        self.raycaster = Raycaster(self.window, self.maze, self.config, 
                                   self.start_coords, self.end_coords)

        # --- Timer Variables ---
        self.game_started_time = 0 
        self.game_finished_time = 0 
        self.game_completed = False 
        self.elapsed_time_ms = 0 

        # --- UI Fonts ---
        # Larger font for the main timer
        self.timer_font = pygame.font.Font(None, 48) 
        # Smaller font for general messages like "MAZE COMPLETED!"
        self.message_font = pygame.font.Font(None, 72)


    def _get_start_angle(self) -> float:
        """
        Determines the initial angle of the player based on maze start point
        or a default.
        """
        return 0.0

    def _pre_render_minimap(self) -> pygame.Surface:
        """
        Renders the static maze layout to a separate surface once.
        """
        minimap_width = self.maze.width * self.tile_size
        minimap_height = self.maze.height * self.tile_size
        minimap_surf = pygame.Surface((minimap_width, minimap_height), pygame.SRCALPHA)

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                color = (200, 200, 200) if self.maze.grid[y][x] == 1 else (0, 0, 0)
                # Draw start/end blocks on minimap for debug
                if (x, y) == self.start_coords:
                    color = (0, 255, 0) # Green for start
                elif (x, y) == self.end_coords:
                    color = (255, 0, 0) # Red for end
                pygame.draw.rect(minimap_surf, color, pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
        return minimap_surf


    def update(self, events: list[pygame.event.Event]) -> str | None:
        """
        Updates the game logic, processes player input, and manages game state.

        Args:
            events (list[pygame.event.Event]): A list of all Pygame events for the current frame.

        Returns:
            str | None: An action string (e.g., "pause"), or None.
        """
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "pause"

        if not self.game_completed:
            self.player.update()

            # Start timer when player makes first move (or is not at initial position)
            if self.game_started_time == 0 and (abs(self.player.x - (self.start_coords[0] + 0.5)) > 0.01 or abs(self.player.y - (self.start_coords[1] + 0.5)) > 0.01):
                self.game_started_time = pygame.time.get_ticks()
            
            # Update elapsed time if game has started
            if self.game_started_time > 0:
                self.elapsed_time_ms = pygame.time.get_ticks() - self.game_started_time

            # Check for game completion
            if self.player.check_end_condition(self.end_coords):
                self.game_completed = True
                self.game_finished_time = pygame.time.get_ticks()
                self.elapsed_time_ms = self.game_finished_time - self.game_started_time
                print(f"Maze Completed! Time: {self._format_time(self.elapsed_time_ms)}")
        
        return None

    def _format_time(self, milliseconds: int) -> str:
        """Formats milliseconds into MM:SS.ms string."""
        total_seconds = milliseconds // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        milliseconds_remainder = milliseconds % 1000 # Milliseconds part
        return f"{minutes:02}:{seconds:02}.{milliseconds_remainder:03}"


    def draw(self):
        """
        Renders the game visuals. This will primarily involve the raycaster.
        A debug minimap is drawn for development.
        """
        # Call Raycaster to draw the 3D view
        self.raycaster.render(self.player.pos, self.player.angle)

        # --- Draw In-Game UI Elements ---

        # 1. Minimap (if debug enabled)
        if GameConstants.DEBUG_DRAW_MINIMAP: 
            minimap_width, minimap_height = self._minimap_surface.get_size()
            padding = 20
            # Position in lower-left corner
            minimap_x = padding
            minimap_y = self.window.get_height() - minimap_height - padding
            
            # Optional: Draw a semi-transparent background for minimap
            bg_rect = pygame.Rect(minimap_x - 5, minimap_y - 5, minimap_width + 10, minimap_height + 10)
            pygame.draw.rect(self.window, (0, 0, 0, 128), bg_rect) # Black with 50% opacity
            
            self.window.blit(self._minimap_surface, (minimap_x, minimap_y))
            self._draw_player_on_minimap(offset_x=minimap_x, offset_y=minimap_y) # Pass offset


        # 2. Timer Display
        timer_text = self._format_time(self.elapsed_time_ms)
        text_surface = self.timer_font.render(f"Time: {timer_text}", True, (255, 255, 255))
        
        padding = 20
        # Position the timer in the lower-right corner
        text_rect = text_surface.get_rect(bottomright=(self.window.get_width() - padding, self.window.get_height() - padding))
        
        # Optional: Draw a semi-transparent background for the timer
        timer_bg_rect = text_rect.inflate(20, 10) # Inflate by 10 pixels horizontally, 5 vertically on each side
        pygame.draw.rect(self.window, (0, 0, 0, 128), timer_bg_rect, border_radius=5) # Black with 50% opacity
        
        self.window.blit(text_surface, text_rect)

        # 3. "Maze Completed!" message
        if self.game_completed:
            completion_text = self.message_font.render("MAZE COMPLETED!", True, (0, 255, 0))
            completion_rect = completion_text.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
            
            # Optional: Draw a semi-transparent background for completion message
            completion_bg_rect = completion_rect.inflate(40, 20)
            pygame.draw.rect(self.window, (0, 0, 0, 150), completion_bg_rect, border_radius=10)
            
            self.window.blit(completion_text, completion_rect)


    def _draw_player_on_minimap(self, offset_x: int = 0, offset_y: int = 0):
        """
        Draws the player's position and direction on the minimap,
        applying an offset for minimap's position on screen.
        """
        player_screen_x = int(self.player.x * self.tile_size) + offset_x
        player_screen_y = int(self.player.y * self.tile_size) + offset_y

        pygame.draw.circle(self.window, (255, 255, 255), (player_screen_x, player_screen_y), 5)

        line_length = 20
        end_x = player_screen_x + line_length * math.cos(self.player.angle)
        end_y = player_screen_y + line_length * math.sin(self.player.angle)
        pygame.draw.line(self.window, (255, 0, 0), (player_screen_x, player_screen_y), (int(end_x), int(end_y)), 2)