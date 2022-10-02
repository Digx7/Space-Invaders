import pygame as pg
from pygame.sprite import Sprite, Group
from timer import Timer
from random import randint

class Lasers:
    def __init__(self, settings):
        self.lasers = Group()
        self.settings = settings
    def reset(self):
        self.lasers.empty()        
    def shoot(self, settings, screen, ship, sound):
        self.lasers.add(Laser(settings=settings, screen=screen, ship=ship, sound=sound))
    def update(self):
        self.lasers.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0: self.lasers.remove(laser)
    def draw(self):
        for laser in self.lasers.sprites(): laser.draw()

class Laser(Sprite):
    """A class to manage lasers fired from the ship"""
    laser_images = [pg.transform.rotozoom(pg.image.load(f'images/laser_{n}.png'), 0, 1) for n in range(4)]
    
    def __init__(self, settings, screen, ship, sound):
        super().__init__()
        self.screen = screen
        self.rect = pg.Rect(0, 0, settings.laser_width, settings.laser_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top
        self.y = float(self.rect.y)
        self.color = (randint(0, 200), randint(0, 200), randint(0, 200))
        self.speed_factor = settings.laser_speed_factor

        self.timer = Timer(image_list=Laser.laser_images, delay=400)
        sound.shoot_laser()

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y
        self.draw()
    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
        # pg.draw.rect(self.screen, self.color, self.rect)
