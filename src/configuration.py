import os
import configparser
import pygame as pg


class Config:
    def __init__(self):
        config_file = "config.ini"

        self.config = configparser.ConfigParser()

        if not os.path.exists(config_file):
            self.config["windows parameters"] = {
                "width": 1280,
                "height": 720,
                "window_mode": 0,
                "fps": 0,
            }
            with open(config_file, "w") as configfile:
                self.config.write(configfile)

        else:
            self.config.read(config_file)

    def getResolution(self):
        width = self.config.getint("windows parameters", "width")
        height = self.config.getint("windows parameters", "height")
        return width, height

    def getWindowMode(self):
        modes = {0: pg.SHOWN, 1: pg.NOFRAME, 2: pg.FULLSCREEN}
        mode = self.config.getint("windows parameters", "window_mode")
        return modes.get(mode)

    def getFPSLock(self):
        fps = self.config.getint("windows parameters", "fps")
        return fps
