import pygame
import math

from src.game.game_logic.player import Player

class GameLogic:
    def __init__(self, maze_data):
        self.maze_data = maze_data
        self.pos_x, self.pos_y = maze_data["start"]
        self.pos_x += 0.5
        self.pos_y += 0.5
        self.angle = self.get_start_angle()
        self.speed = 0.05
        self.rotation_speed = 0.05
        self.draw_distance = 3

        self.player = Player((self.pos_x, self.pos_y), self.angle, self.maze_data["maze"])

    def get_start_angle(self):
        return 0

    def check_collision(self, new_x, new_y):
        """Check if the player's new position collides with a wall."""
        grid_x = int(new_x)
        grid_y = int(new_y)

        if (
            0 <= grid_x < self.maze_data["maze"].width
            and 0 <= grid_y < self.maze_data["maze"].height
            and self.maze_data["maze"].grid[grid_y][grid_x] == 0
        ):
            return False
        return True

    def update_position(self, dx, dy):
        new_x = self.pos_x + dx
        new_y = self.pos_y + dy

        if not self.check_collision(new_x, new_y):
            self.pos_x = new_x
            self.pos_y = new_y

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            return "pause"

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dx = self.speed * math.cos(self.angle)
            dy = self.speed * math.sin(self.angle)
            self.update_position(dx, dy)

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dx = -self.speed * math.cos(self.angle)
            dy = -self.speed * math.sin(self.angle)
            self.update_position(dx, dy)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle -= self.rotation_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle += self.rotation_speed

        return {"map": self.get_visible_map(), "player_angle": self.angle}

    def get_visible_map(self):
        """Returns a section of the map with the player at the center and blocks within draw_distance radius."""
        center_x = int(self.pos_x)
        center_y = int(self.pos_y)
        radius = self.draw_distance

        visible_map = []
        for y in range(center_y - radius, center_y + radius + 1):
            row = []
            for x in range(center_x - radius, center_x + radius + 1):
                if 0 <= y < self.maze_data["maze"].height and 0 <= x < self.maze_data["maze"].width:
                    row.append(self.maze_data["maze"].grid[y][x])
                else:
                    row.append(1)  # Represents out-of-bounds areas
            visible_map.append(row)

        return visible_map

    def draw(self, screen):
        """Visualizes the map, player, and their direction."""
        tile_size = 10

        for y in range(self.maze_data["maze"].height):
            for x in range(self.maze_data["maze"].width):
                color = (200, 200, 200) if self.maze_data["maze"].grid[y][x] == 1 else (0, 0, 0)
                pygame.draw.rect(screen, color, pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))

        pygame.draw.circle(screen, (255, 255, 255), (int(self.pos_x * tile_size), int(self.pos_y * tile_size)), 5)

        line_length = 50
        end_x = self.pos_x * tile_size + line_length * math.cos(self.angle)
        end_y = self.pos_y * tile_size + line_length * math.sin(self.angle)
        pygame.draw.line(screen, (255, 0, 0), (int(self.pos_x * tile_size), int(self.pos_y * tile_size)), (int(end_x), int(end_y)), 2)
