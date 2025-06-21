from src.game.screens.menu import Menu

class GameOverMenu(Menu):
    def __init__(self, window, score):
        options = self.add_options(score)
        super().__init__(window, options)

    def add_options(self, score):
        """Adds game over score and return to main menu options."""
        options = []

        options.append({"option": f"Total Time: {(score['total_time'] / 1000):.2f}s", "event": None})

        options.append({"option": "Return to Main Menu", "event": "main_menu"})

        return options