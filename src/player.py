class Player:
    def __init__(self):
        self.player_position = None
        self.player_angle = 0

    def set_position(self, x, y):
        self.player_position = self.x, self.y = x, y

    def get_position(self):
        return self.player_position

    def set_angle(self, angle):
        self.player_angle = angle

    def get_angle(self):
        return self.player_angle
