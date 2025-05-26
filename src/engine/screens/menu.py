import pygame

class Menu:
    def __init__(self, window, options):
        self.window = window
        self.options = options
        self.current_index = 0
        self.last_input_time = pygame.time.get_ticks()
        self.input_cooldown = 200

    def reset_cooldown(self):
        """Resets the input cooldown for menu, typically called when re-entering the menu."""
        self.last_input_time = pygame.time.get_ticks()

    def update(self, event):
        """Handles arrow key navigation and selection."""
        current_time = pygame.time.get_ticks()

        if event.type == pygame.KEYDOWN and current_time - self.last_input_time > self.input_cooldown:
            self.last_input_time = current_time  # Update cooldown timer
            
            if event.key == pygame.K_UP:  # Move up
                self.current_index = (self.current_index - 1) % len(self.options)

            elif event.key == pygame.K_DOWN:  # Move down
                self.current_index = (self.current_index + 1) % len(self.options)

            elif event.key == pygame.K_RETURN:  # Select option
                return self.options[self.current_index]["event"]
            
        return None

    def draw(self):
        """Renders menu items with selection highlighting."""
        font = pygame.font.Font(None, 48)

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.current_index else (150, 150, 150)
            text_surface = font.render(option["option"], True, color)
            text_rect = text_surface.get_rect(center=(self.window.get_width() // 2, 200 + i * 50))
            self.window.blit(text_surface, text_rect)
