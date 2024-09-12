import sys
import pygame as pg


class Main:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1280, 720))
        self.clock = pg.time.Clock()
        self.delta_time = 1

    def update(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

        pg.display.flip()

        self.delta_time = self.clock.tick(0)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill((0, 0, 0))

    def run(self):
        while True:
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Main()
    game.run()
