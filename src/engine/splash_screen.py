import pygame

class SplashScreen:
    def __init__(self, screen):
        self.screen = screen
        self.sequence = [
            {"text": "UziWares Presents", "font_size": 64},
            {"text": "A game by Uzair & Srujan", "font_size": 48},
            {"text": "A-Maze", "font_size": 128}
        ]
        self.current_index = 0
        self.display_duration = 2000
        self.start_time = pygame.time.get_ticks()
        self.alpha = 0

    def update(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        
        if elapsed_time < 1000:
            self.alpha = min(255, int((elapsed_time / 1000) * 255))
        else:
            self.alpha = 255
        
        if elapsed_time > self.display_duration:
            self.current_index += 1
            self.start_time = pygame.time.get_ticks()
            self.alpha = 0

        return self.current_index < len(self.sequence)

    def draw(self):
        if self.current_index < len(self.sequence):
            splash = self.sequence[self.current_index]
            font = pygame.font.Font(None, splash["font_size"])
            text_surface = font.render(splash["text"], True, (255, 255, 255))

            text_surface.set_alpha(self.alpha)

            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(text_surface, text_rect)
