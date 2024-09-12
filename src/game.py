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

    def collision_check(self):
        return False

    def update(self):
        angle = self.player.get_angle()
        position = self.player.get_position()

        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        sin_b = math.sin(angle + (math.pi / 2))
        cos_b = math.cos(angle + (math.pi / 2))

        speed = (1 / 400) * self.game.delta_time  # fix player speed to config
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
            angle -= (
                math.pi / 2000
            ) * self.game.delta_time  ## fix rotation speed to config

        if keys[pg.K_RIGHT]:
            angle += (
                math.pi / 2000
            ) * self.game.delta_time  ## fix rotation speed to config

        if not self.collision_check():
            x = position[0] + dx
            y = position[1] + dy

            self.player.set_position(x, y)
            self.player.set_angle(angle)

    ## draw 2d
    def draw(self):
        angle = self.player.get_angle()
        position = self.player.get_position()

        pg.draw.circle(
            self.game.screen, "green", (position[0] * 10, position[1] * 10), 5
        )

        pg.draw.line(
            self.game.screen,
            "red",
            (position[0] * 10, position[1] * 10),
            (
                position[0] * 10 + 20 * 10 * math.cos(angle),
                position[1] * 10 + 20 * 10 * math.sin(angle),
            ),
            1,
        )
