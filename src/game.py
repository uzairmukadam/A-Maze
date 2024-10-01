import pygame as pg
import math

import map
import player


class Game:
    def __init__(self, game):
        self.map = None
        self.player = None
        self.raycaster = None
        self.renderer = None

        self.game = game

        self.load_game()

    def load_game(self):
        self.map = map.Map()
        self.player = player.Player()

        self.map.load_map()
        self.player.set_position(self.map.start[0], self.map.start[1])

    def collision_check(self, position, dx, dy):
        safe_distance = 0.3
        x = position[0] + dx
        y = position[1] + dy

        if x >= 0 and y >= 0:
            i = int(x + safe_distance * (1 if dx > 0 else -1))
            j = int(y + safe_distance * (1 if dy > 0 else -1))

            if self.map.map[j][i] != 1:
                self.player.set_position(x, y)

    def check_exit(self, position):
        i = int(position[0])
        j = int(position[1])

        if (i, j) == self.map.exit_block:
            print("Exit")
        else:
            print("Null")

    def update(self):
        angle = self.player.get_angle()
        position = self.player.get_position()

        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        sin_b = math.sin(angle + (math.pi / 2))
        cos_b = math.cos(angle + (math.pi / 2))

        speed = self.game.config.getPlayerSpeed() * self.game.delta_time
        sin_speed = speed * sin_a
        cos_speed = speed * cos_a
        sin_side_speed = speed * sin_b * 0.5
        cos_side_speed = speed * cos_b * 0.5

        dx, dy = 0, 0

        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            dx += cos_speed
            dy += sin_speed

        if keys[pg.K_s]:
            dx -= cos_speed
            dy -= sin_speed

        if keys[pg.K_a]:
            dx -= cos_side_speed
            dy -= sin_side_speed

        if keys[pg.K_d]:
            dx += cos_side_speed
            dy += sin_side_speed

        if keys[pg.K_LEFT]:
            angle -= (self.game.config.getRotationSpeed()) * self.game.delta_time

        if keys[pg.K_RIGHT]:
            angle += (self.game.config.getRotationSpeed()) * self.game.delta_time

        self.collision_check(position, dx, dy)

        self.player.set_angle(angle)

        position = self.player.get_position()

        if keys[pg.K_SPACE]:
            self.check_exit(position)

    ## draw 2d
    def draw(self):
        scale = 20
        angle = self.player.get_angle()
        position = self.player.get_position()

        ## drawing map
        for y in range(20):
            for x in range(20):
                if self.map.map[y][x] == 1:
                    pg.draw.rect(
                        self.game.screen, "white", (x * scale, y * scale, scale, scale)
                    )
                else:
                    pg.draw.rect(
                        self.game.screen,
                        "yellow",
                        (x * scale, y * scale, scale, scale),
                        1,
                    )

        ## drawing player
        pg.draw.circle(
            self.game.screen, "green", (position[0] * scale, position[1] * scale), 5
        )

        pg.draw.line(
            self.game.screen,
            "red",
            (position[0] * scale, position[1] * scale),
            (
                position[0] * scale + 20 * scale * math.cos(angle),
                position[1] * scale + 20 * scale * math.sin(angle),
            ),
            1,
        )
