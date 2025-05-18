import pygame

class InputHandler:
    def __init__(self):
        self.key_map = {
            pygame.K_UP: "move_up",
            pygame.K_DOWN: "move_down",
            pygame.K_LEFT: "move_left",
            pygame.K_RIGHT: "move_right",
            pygame.K_RETURN: "select",
            pygame.K_ESCAPE: "quit"
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            return self.key_map.get(event.key, None)
        return None
