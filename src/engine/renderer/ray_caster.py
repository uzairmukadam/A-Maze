import math


class Ray:
    def __init__(self, angle, hit_wall, hit_x, hit_y, wall_x, distance):
        self.angle = angle
        self.hit_wall = hit_wall
        self.hit_x = hit_x
        self.hit_y = hit_y
        self.wall_x = wall_x
        self.distance = distance

class RayCaster:
    def __init__(self, num_rays, fov):
        self.num_rays = num_rays
        self.fov = fov

        self.angle_increment = fov / num_rays

    def cast_ray(self, map, angle):
        dx = math.cos(angle)
        dy = math.sin(angle)

        map_x = 0
        map_y = 0

        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1

    def update(self, map, angle):
        rays = []
        start_angle = angle - self.fov / 2

        for i in range(self.num_rays):
            ray_angle = start_angle + i * self.angle_increment

        return rays

    def draw(self):
        pass
