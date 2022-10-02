import pygame as pg
import pygame.time

from settings import Settings
import game_functions as gf
from pygame.sprite import Group

from laser import Lasers
from ship import Ship
from sound import Sound
from Alien import Aliens
from Bunker import Bunkers
from game_stats import GameStats
from button import Buttons
from UI import *


class Game:
    def __init__(self):
        # initialize pygame and set up screen
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        # set up frame rate
        self.clock = pg.time.Clock()
        self.clock.tick(self.settings.fps)
        pygame.time.set_timer(pygame.USEREVENT, 500)

        # set up UI
        self.stats = GameStats(self.settings)

        self.game_ui = GameUI(self.settings, self.screen, self.stats)
        self.start_ui = StartUI(self.settings, self.screen, self.stats)
        self.end_ui = EndUI(self.settings, self.screen, self.stats)

        self.sound = Sound(bg_music="sounds/Space_Invaders_Remix.mp3")

        laser_group = Group()
        self.lasers = Lasers(laser_group, self.settings)

        self.ship = Ship(self.settings, self.screen, self.sound, self.lasers)

        alien_group = Group()
        alien_laser_group = Group()
        self.alien_lasers = Lasers(alien_laser_group, self.settings)
        self.aliens = Aliens(self.screen, alien_group, self.settings, self.sound, self.alien_lasers)

        bunker_group = Group()
        self.bunkers = Bunkers(bunker_group)

    def play(self):
        self.sound.play_bg()
        while True:
            if self.stats.is_current_scene("menu"):
                gf.start_menu_update(self)
                gf.start_menu_draw(self)
            elif self.stats.is_current_scene("main"):
                gf.main_update(self)
                gf.main_draw(self)
            elif self.stats.is_current_scene("end"):
                gf.end_update(self)
                gf.end_draw(self)
            # self.clock.tick(self.settings.fps)
            pg.display.flip()


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
