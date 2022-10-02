import random

import pygame as pg
from pygame import gfxdraw

import sys
from PIL import Image, ImageDraw

from pygame.sprite import Sprite


class Bunkers:
    def __init__(self, bunker_group):
        self.bunkers = bunker_group

    def spawn(self, bunker):
        self.bunkers.add(bunker)

    def draw(self):
        for bunker in self.bunkers.sprites():
            bunker.draw()


class Bunker(Sprite):
    """A class to represent a single bunker"""
    def __init__(self, settings, screen):
        super(Bunker, self).__init__()
        self.settings = settings
        self.screen = screen

        self.max_health = self.settings.starting_bunker_health
        self.current_health = self.max_health

        self.deteriorate()
        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def kill(self):
        self.current_health -= 1
        self.deteriorate()

        if self.current_health <= 0:
            Sprite.kill(self)

    def deteriorate(self):
        target = self.current_health
        if self.current_health <= 0:
            target = 1
        self.image = self.settings.sprites[f"cover{target}"]

    def draw(self):
        self.screen.blit(self.image, self.rect)
