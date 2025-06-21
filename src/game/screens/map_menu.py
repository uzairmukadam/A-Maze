from src.game.screens.menu import Menu

class MapMenu(Menu):
    def __init__(self, window, maps):
        options = self.add_options(maps)
        super().__init__(window, options)

    def add_options(self, maps):
        """Dynamically adds map options and a 'Back' option to the menu."""
        options = []

        for map_item in maps:
            name = map_item["data"]["mazeName"]
            event = map_item["id"]

            option = {"option": name, "event": event}
            options.append(option)

        options.append({"option": "Back", "event": "main_menu"})

        return options