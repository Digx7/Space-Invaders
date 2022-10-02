import random

import pygame
from pygame.sprite import Sprite
from Animation import *


class Aliens:
    def __init__(self, screen, alien_group, settings, sound, lasers=None):
        self.screen = screen

        self.aliens = alien_group
        self.lasers = lasers
        self.sound = sound
        self.settings = settings

        self.lasers_attempted = 0

    def spawn(self, alien):
        self.aliens.add(alien)

    def freeze(self):
        self.lasers.freeze()
        for alien in self.aliens:
            alien.freeze()

    def update(self):
        self.check_fleet_edges()
        self.aliens.update()
        self.shoot()
        # TODO

    def update_animations(self):
        for alien in self.aliens.sprites():
            alien.update_animation()

    def draw(self):
        for alien in self.aliens.sprites():
            alien.draw()

    def check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.alien_type == "ufo" and alien.rect.left >= self.settings.screen_width:
                self.aliens.remove(alien)
        for alien in self.aliens.sprites():
            if not alien.alien_type == "ufo" and alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed_factor
        self.settings.alien_move_direction *= -1

    def shoot(self):
        self.lasers_attempted += 1
        if self.lasers_attempted % self.settings.alien_lasers_every == 0 and len(self.aliens) > 0:
            self.num = random.randint(0, len(self.aliens))
            c_num = 0
            for alien in self.aliens.sprites():
                c_num +=1
                if c_num == self.num: self.source = alien

            if self.source.moving:
                self.lasers.shoot(settings=self.settings, screen=self.screen, ship=self.source, sound=self.sound, speed=self.settings.alien_laser_speed_factor)



class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    def __init__(self, settings, stats, screen, alien_type="default"):
        """Initialize the alien and set its starting position."""

        super(Alien, self).__init__()
        self.screen = screen
        self.settings = settings
        self.stats = stats

        self.moving = True
        self.dying = False

        self.alien_type = alien_type
        self.inialize_animations()

        self.update_animation()
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

        self.initialize_score_amount()

    def inialize_animations(self):
        if self.alien_type == "default":
            self.Idle_Anim = Animation([self.settings.sprites["alien1_move1"], self.settings.sprites["alien1_move2"]])
            self.Death_Anim = Animation([self.settings.sprites["alien1_dead1"], self.settings.sprites["alien1_dead2"]], 1)
        elif self.alien_type == "02":
            self.Idle_Anim = Animation([self.settings.sprites["alien2_move1"], self.settings.sprites["alien2_move2"]])
            self.Death_Anim = Animation([self.settings.sprites["alien2_dead1"], self.settings.sprites["alien2_dead2"]], 1)
        elif self.alien_type == "03":
            self.Idle_Anim = Animation([self.settings.sprites["alien3_move1"], self.settings.sprites["alien3_move2"]])
            self.Death_Anim = Animation([self.settings.sprites["alien3_dead1"], self.settings.sprites["alien3_dead2"]], 1)
        elif self.alien_type == "ufo":
            self.Idle_Anim = Animation([self.settings.sprites["ufo_move1"], self.settings.sprites["ufo_move2"]])
            self.Death_Anim = Animation([self.settings.sprites["ufo_dead1"], self.settings.sprites["ufo_dead2"]],
                                        1)


        self.Animations = Animations(idle=self.Idle_Anim, death=self.Death_Anim)

    def initialize_score_amount(self):
        if self.alien_type == "default": self.score = self.settings.alien1_points
        elif self.alien_type == "02": self.score = self.settings.alien2_points
        elif self.alien_type == "03": self.score = self.settings.alien3_points
        elif self.alien_type == "ufo": self.score = self.settings.ufo_points

    def update(self):

        # Move the alien
        if self.moving and not self.alien_type == "ufo":
            self.x += (self.settings.alien_left_right_speed_factor * self.settings.alien_move_direction)
        elif self.moving and self.alien_type == "ufo":
            self.x += self.settings.ufo_speed_factor
        self.rect.x = self.x

        if self.dying and self.Animations.check_if_fin():
            self.stats.current_score += self.score
            Sprite.kill(self)
            print("I should be dead")

        self.draw()
        # TODO

    def kill(self):
        if not self.dying:
            self.Animations.set_current_animation("death")
            self.dying = True

    def freeze(self):
        self.moving = False

    def draw(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def update_animation(self):
        self.image = self.Animations.get_current_animation().update()

    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
