import pygame
import math

from src.game.game_logic.player import Player
from src.game.constants import Constants 

class GameLogic:
    """
    Manages core game logic, including maze, player, and game state.
    Renders 3D walls using raycasting with DDA, distance-based fading,
    and pulsating highlight for the end block. Includes a timer display.
    """
    def __init__(self, window, config, maze):
        self.window = window
        self.config = config 
        self.maze = maze

        self.player = Player(self.maze)
        
        self.game_start_time = 0
        self.total_time = 0

        self.screen_width, self.screen_height = self.window.get_size()
        self.half_screen_height = self.screen_height // 2

        self.fov = math.radians(Constants.DEFAULT_FOV)
        self.half_fov = self.fov / 2
        self.angle_increment = self.fov / self.screen_width

        self.dist_to_proj_plane = (self.screen_width / 2) / math.tan(self.half_fov)

        self.maze_data = maze["mazeData"]
        self.maze_width = len(self.maze_data[0]) if self.maze_data else 0
        self.maze_height = len(self.maze_data) if self.maze_data else 0
        self.start_coord = maze["startCoordinate"]
        self.end_coord = maze["endCoordinate"]

        self.wall_visual_height_pixels = self.screen_height * Constants.WALL_MAX_VIEWPORT_HEIGHT_RATIO

        pygame.font.init()
        self.timer_font = pygame.font.Font(None, 36)

    def get_score(self):
        return self.total_time

    def update(self, events):
        player_at_start_pos = (self.player.x == self.player.maze_start[0] + 0.5 and
                               self.player.y == self.player.maze_start[1] + 0.5)

        if self.game_start_time == 0 and not player_at_start_pos:
            self.game_start_time = pygame.time.get_ticks()

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "pause"
            
        action = self.player.update()
        if action == "end":
            game_end_time = pygame.time.get_ticks()
            self.total_time = game_end_time - self.game_start_time
            return "game_over"

        return None

    def draw(self):
        self._draw_ceiling_and_floor_background()
        self._draw_walls_raycasting()
        self.draw_timer()

    def _draw_ceiling_and_floor_background(self):
        pygame.draw.rect(self.window, Constants.CEILING_COLOR, (0, 0, self.screen_width, self.half_screen_height))
        pygame.draw.rect(self.window, Constants.FLOOR_COLOR, (0, self.half_screen_height, self.screen_width, self.half_screen_height))

    def _is_adjacent_to_point(self, wall_x, wall_y, target_x, target_y):
        dx = abs(wall_x - target_x)
        dy = abs(wall_y - target_y)
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def _cast_single_ray(self, start_pos_x, start_pos_y, ray_angle):
        cos_ray = math.cos(ray_angle)
        sin_ray = math.sin(ray_angle)

        map_x = int(start_pos_x)
        map_y = int(start_pos_y)

        side_dist_x = 0.0
        side_dist_y = 0.0

        delta_dist_x = abs(1.0 / cos_ray) if abs(cos_ray) > 1e-6 else float('inf')
        delta_dist_y = abs(1.0 / sin_ray) if abs(sin_ray) > 1e-6 else float('inf')

        step_x = 0
        step_y = 0

        if cos_ray < 0:
            step_x = -1
            side_dist_x = (start_pos_x - map_x) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_x + 1.0 - start_pos_x) * delta_dist_x

        if sin_ray < 0:
            step_y = -1
            side_dist_y = (start_pos_y - map_y) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_y + 1.0 - start_pos_y) * delta_dist_y

        hit = False
        hit_side = -1 
        
        current_ray_distance = 0.0 
        
        final_hit_map_x, final_hit_map_y = -1, -1

        for _ in range(int(Constants.MAX_RAY_DISTANCE) * 2 + 2): 
            if current_ray_distance >= Constants.MAX_RAY_DISTANCE:
                hit = False 
                break

            if side_dist_x < side_dist_y:
                current_ray_distance = side_dist_x
                side_dist_x += delta_dist_x
                map_x += step_x
                hit_side = 0
            else:
                current_ray_distance = side_dist_y
                side_dist_y += delta_dist_y
                map_y += step_y
                hit_side = 1

            if 0 <= map_y < self.maze_height and 0 <= map_x < self.maze_width:
                if self.maze_data[map_y][map_x] == 1:
                    hit = True
                    final_hit_map_x, final_hit_map_y = map_x, map_y
                    break
            else:
                hit = True
                final_hit_map_x, final_hit_map_y = map_x, map_y
                break
        
        ray_hit_distance = 0.0
        if hit:
            ray_hit_distance = current_ray_distance
        else:
            ray_hit_distance = Constants.MAX_RAY_DISTANCE

        ray_hit_distance = max(Constants.CLIP_PLANE_DISTANCE, min(ray_hit_distance, Constants.MAX_RAY_DISTANCE))
        
        return ray_hit_distance, final_hit_map_x, final_hit_map_y, hit_side

    def _draw_walls_raycasting(self):
        player_x, player_y, player_angle = self.player.x, self.player.y, self.player.angle
        end_x, end_y = self.end_coord[0], self.end_coord[1]
        
        ray_angle = player_angle - (self.fov / 2)

        for ray_idx in range(self.screen_width):
            ray_hit_distance, hit_map_x, hit_map_y, hit_side = self._cast_single_ray(player_x, player_y, ray_angle)
            
            perp_dist_for_3d = ray_hit_distance * math.cos(ray_angle - player_angle)
            
            if perp_dist_for_3d <= 0: perp_dist_for_3d = Constants.CLIP_PLANE_DISTANCE 

            wall_screen_height = self.wall_visual_height_pixels / perp_dist_for_3d
            
            wall_top = self.half_screen_height - (wall_screen_height / 2)
            wall_bottom = self.half_screen_height + (wall_screen_height / 2)

            wall_top = max(0, int(wall_top))
            wall_bottom = min(self.screen_height, int(wall_bottom))

            base_color = Constants.WALL_COLOR

            is_end_wall = False
            if hit_map_x != -1 and hit_map_y != -1 and \
               0 <= hit_map_y < self.maze_height and 0 <= hit_map_x < self.maze_width:
                if self._is_adjacent_to_point(hit_map_x, hit_map_y, end_x, end_y):
                    is_end_wall = True

            if is_end_wall:
                pulse_factor = (math.sin(pygame.time.get_ticks() / 200.0) + 1.0) / 2.0
                
                r = int(Constants.END_WALL_COLOR[0] * (1 - pulse_factor) + Constants.END_WALL_GLOW_COLOR[0] * pulse_factor)
                g = int(Constants.END_WALL_COLOR[1] * (1 - pulse_factor) + Constants.END_WALL_GLOW_COLOR[1] * pulse_factor)
                b = int(Constants.END_WALL_COLOR[2] * (1 - pulse_factor) + Constants.END_WALL_GLOW_COLOR[2] * pulse_factor)
                base_color = (r, g, b)
            
            fade_factor = max(0.0, min(1.0, (ray_hit_distance - Constants.FADE_START_DISTANCE) / 
                                        (Constants.MAX_RAY_DISTANCE - Constants.FADE_START_DISTANCE)))
            
            draw_color = (int(base_color[0] * (1 - fade_factor)),
                          int(base_color[1] * (1 - fade_factor)),
                          int(base_color[2] * (1 - fade_factor)))


            pygame.draw.line(self.window, draw_color, (ray_idx, wall_top), (ray_idx, wall_bottom), 1)
            
            ray_angle += self.angle_increment

    def draw_timer(self):
        elapsed_time_ms = 0
        if self.game_start_time != 0: 
            elapsed_time_ms = pygame.time.get_ticks() - self.game_start_time
        
        minutes = elapsed_time_ms // 60000
        seconds = (elapsed_time_ms % 60000) // 1000
        milliseconds = elapsed_time_ms % 1000

        time_text = f"Time: {minutes:02d}:{seconds:02d}:{milliseconds:03d}"

        text_surface = self.timer_font.render(time_text, True, (255, 255, 255))

        text_rect = text_surface.get_rect()
        
        padding = 10
        text_rect.bottomleft = (padding, self.screen_height - padding)

        self.window.blit(text_surface, text_rect)

    def draw_temp(self):
        scale = 25

        for y, row in enumerate(self.maze_data):
            for x, col in enumerate(row):
                if col == 1:
                    pygame.draw.rect(self.window, (255, 255, 255), (x * scale, y * scale, scale, scale))

        start = self.maze["startCoordinate"]
        pygame.draw.rect(self.window, (0, 255, 0), (start[0] * scale, start[1] * scale, scale, scale))
        end = self.maze["endCoordinate"]
        pygame.draw.rect(self.window, (255, 0, 0), (end[0] * scale, end[1] * scale, scale, scale))

        pos_x = self.player.x
        pos_y = self.player.y

        pygame.draw.circle(self.window, (255, 0, 0), (int(pos_x * scale), int(pos_y * scale)), 5)
        
        num_rays_2d_viz = 50 
        angle_increment_2d_viz = self.fov / num_rays_2d_viz
        ray_angle_2d_viz = self.player.angle - (self.fov / 2)

        for _ in range(num_rays_2d_viz):
            ray_angle_2d_viz %= (2 * math.pi)
            
            ray_hit_distance, hit_map_x, hit_map_y, hit_side = self._cast_single_ray(pos_x, pos_y, ray_angle_2d_viz)
            
            DEPTH_LINE_MAX_LENGTH_2D = 10

            normalized_distance = ray_hit_distance / Constants.MAX_RAY_DISTANCE 
            depth_line_length = max(1, int(DEPTH_LINE_MAX_LENGTH_2D * (1 - normalized_distance)))

            hit_screen_x = int(pos_x * scale + (ray_hit_distance * scale * math.cos(ray_angle_2d_viz)))
            hit_screen_y = int(pos_y * scale + (ray_hit_distance * scale * math.sin(ray_angle_2d_viz)))

            pygame.draw.line(self.window, (255, 255, 0), 
                             (hit_screen_x, hit_screen_y - depth_line_length // 2), 
                             (hit_screen_x, hit_screen_y + depth_line_length // 2), 1)

            pygame.draw.line(self.window, (100, 100, 255),
                             (int(pos_x * scale), int(pos_y * scale)), 
                             (hit_screen_x, hit_screen_y), 1)
            
            ray_angle_2d_viz += angle_increment_2d_viz

    def draw_mini_map(self):
        self.draw_temp()
