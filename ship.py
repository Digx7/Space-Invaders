import pygame
from pygame.sprite import Sprite
from game_functions import clamp
from vector import Vector
from Animation import *


class Ship(Sprite):
    def __init__(self, settings, screen, sound, lasers=None):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.sound = sound

        self.moving = True

        self.Idle_Anim = Animation([settings.sprites["ship_move1"], settings.sprites["ship_move2"]])
        self.Death_Anim = Animation([settings.sprites["ship_dead1"], settings.sprites["ship_dead2"],
                                     settings.sprites["ship_dead3"], settings.sprites["ship_dead4"]], 1)

        self.Animations = Animations(idle=self.Idle_Anim, death=self.Death_Anim)

        self.update_animation()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.posn = self.center_ship()    # posn is the centerx, bottom of the rect, not left, top
        self.center_ship()

        self.vel = Vector()
        self.lasers = lasers
        self.shooting = False
        self.lasers_attempted = 0

    def center_ship(self):
        self.shooting = False
        self.vel = Vector()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        new_posn = Vector(self.rect.left, self.rect.top)
        self.posn = new_posn
        return new_posn

    def kill(self):
        self.Animations.set_current_animation("death")
        self.moving = False

    def update(self):

        if self.moving:
            self.posn += self.vel
        self.posn, self.rect = clamp(self.posn, self.rect, self.settings)
        if self.shooting:
            self.lasers_attempted += 1
            if self.lasers_attempted % self.settings.lasers_every == 0:
                print('shooting lasers')
                self.lasers.shoot(settings=self.settings, screen=self.screen, 
                                  ship=self, sound=self.sound, speed=self.settings.laser_speed_factor)
        self.rect.centerx = self.posn.x + self.rect.width / 2
        self.rect.centery = self.posn.y + self.rect.height / 2

    def update_animation(self):
        self.image = self.Animations.get_current_animation().update()

    def draw(self):
        self.screen.blit(self.image, self.rect)
