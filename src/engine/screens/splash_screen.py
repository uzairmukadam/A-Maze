import pygame

class SplashScreen:
    def __init__(self, window):
        self.window = window

        self.sequence = [{"text": "Made by Uzair", "font_size": 48},
                         {"text": "A-Maze", "font_size": 128}]

        self.current_index = 0
        self.start_time = pygame.time.get_ticks()

        self.duration = 2500
        self.alpha = 0

    def update(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time

        if elapsed_time < 1000:
            self.alpha = min(255, int((elapsed_time / 1000) * 255))
        elif elapsed_time < 1500:
            self.alpha = 255
        else:
            fade_out_time = elapsed_time - 1500
            self.alpha = max(0, int(255 - (fade_out_time / 500) * 255))

        if elapsed_time > self.duration:
            self.current_index += 1
            self.start_time = pygame.time.get_ticks()

        return self.current_index < len(self.sequence)

    def draw(self):
        current_squence = self.sequence[self.current_index]
        font = pygame.font.Font(None, current_squence["font_size"])
        text_surface = font.render(current_squence["text"], True, (255, 255, 255))

        text_surface.set_alpha(self.alpha)

        text_rect = text_surface.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
        self.window.blit(text_surface, text_rect)
