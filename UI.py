import pygame.font
from pygame.sprite import Group

from button import *

from ship import Ship


class GameUI():
    """A Class for displaying UI: Score, Highscore, Lives, etc"""

    def __init__(self, settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        # Font settings
        self.text_color = settings.palette.color["ui"]
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the intial values
        # self.update()

    def update(self):
        self.update_score()
        self.update_high_score()
        self.update_level()
        self.update_lives()

    def draw(self):
        self.show_score()
        self.show_high_score()
        self.show_level()
        self.show_lives()

    def update_score(self):
        """Update the rendered image for score"""
        rounded_score = int(round(self.stats.current_score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def update_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self. settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def update_level(self):
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.settings.bg_color)

        # position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def update_lives(self):
        pass


    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)

    def show_high_score(self):
        self.screen.blit(self.high_score_image, self.high_score_rect)

    def show_level(self):
        self.screen.blit(self.level_image, self.level_rect)

    def show_lives(self):
        for life_number in range(self.stats.lives_left):
            sprite = self.settings.sprites["ship_move1"]
            sprite_rect = sprite.get_rect()
            sprite_rect.y = 10
            sprite_rect.x = (sprite_rect.width + 10) * life_number
            self.screen.blit(sprite, sprite_rect)


class StartUI():
    """A Class for displaying UI during start screen"""

    def __init__(self, settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        self.modes = {"Main":"main_menu", "LeaderBoard": "leaderboard_menu"}
        self.current_mode = self.modes["Main"]

        self.buttons = Buttons(self.settings, self.screen, play_button="Play",
                               score_button="Score Board",
                               leaderboard_back_button="back")

        # Font settings
        self.texts = Texts(self.settings, self.screen)
        self.texts.setup_H1s(title1="Space")
        self.texts.setup_H2s(title2="Invaders", LeaderBoard_Header="Leader-Board")
        self.texts.setup_texts(credit="Developed by: Everette",
                               version_num="1.0",
                               alien1_score=f'{self.settings.alien1_points}',
                               alien2_score=f'{self.settings.alien2_points}',
                               alien3_score=f'{self.settings.alien3_points}',
                               ufo_score="???",
                               score1_label="1st:",
                               score1_value="000",
                               score2_label="2nd:",
                               score2_value="000",
                               score3_label="3rd:",
                               score3_value="000",
                               score4_label="4th:",
                               score4_value="000",
                               score5_label="5th:",
                               score5_value="000",
                               score6_label="6th:",
                               score6_value="000",
                               score7_label="7th:",
                               score7_value="000",
                               score8_label="8th:",
                               score8_value="000",
                               score9_label="9th:",
                               score9_value="000",
                               score10_label="10th:",
                               score10_value="000",
                               )

        self.alien_sprites = {}

        for num in range(1, 4):
            self.alien_sprites[f'alien{num}'] = self.settings.sprites[f'alien{num}_move1']
        self.alien_sprites["ufo"] = self.settings.sprites["ufo_move1"]

    def update(self):
        pass

    def draw(self):
        if self.current_mode == self.modes["Main"]: self.draw_main_menu()
        elif self.current_mode == self.modes["LeaderBoard"]: self.draw_leaderboard_menu()

        self.texts.texts["credit"].msg_image_rect.left = self.screen_rect.left + 10
        self.texts.texts["credit"].msg_image_rect.bottom = self.screen_rect.bottom - 10
        self.texts.texts["version_num"].msg_image_rect.left = self.screen_rect.left + 10
        self.texts.texts["version_num"].msg_image_rect.bottom = self.texts.texts["credit"].msg_image_rect.top

        self.texts.draw_text("credit", "text")
        self.texts.draw_text("version_num", "text")

    def draw_main_menu(self):
        self.texts.draw_text_alignx_center("title1", "H1", 75)
        self.texts.draw_text_alignx_center("title2", "H2", 175)

        self.buttons.draw_button_alignx_center("play_button", 600)
        self.buttons.draw_button_alignx_center("score_button", 700)

        initial_y = 225
        offset_y = 75
        offset_x = 100
        num = 1
        for key in self.alien_sprites:
            sprite = self.alien_sprites[key]
            sprite_rect = self.alien_sprites[key].get_rect()
            sprite_rect.centerx = self.screen_rect.centerx - offset_x
            sprite_rect.centery = initial_y + (offset_y * num)

            if not num == 4:
                self.texts.draw_text_alignx_center(f'alien{num}_score', "text", (initial_y + (offset_y * num)))
            elif num == 4:
                self.texts.draw_text_alignx_center("ufo_score", "text", (initial_y + (offset_y * num)))
            self.screen.blit(sprite, sprite_rect)
            num += 1

    def draw_leaderboard_menu(self):
        self.texts.draw_text_alignx_center("LeaderBoard_Header", "H2", 75)

        initial_y = 100
        offset_y = 50
        offset_x = 150
        for num in range(1,11):
            label_x = self.screen_rect.centerx - offset_x
            value_x = self.screen_rect.centerx + offset_x
            y = initial_y + (num * offset_y)

            if num < len(self.stats.scores):
                self.texts.update_text(f'score{num}_value', "text", f'{self.stats.scores[num - 1]}')

            self.texts.draw_text_absolute(f'score{num}_label', "text", (label_x, y))
            self.texts.draw_text_absolute(f'score{num}_value', "text", (value_x, y))

        self.buttons.draw_button_alignx_center("leaderboard_back_button", 700)


class EndUI():

    def __init__(self, settings, screen, stats):
        self.settings = settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.stats = stats

        self.texts = Texts(self.settings, self.screen)
        self.texts.setup_H1s(end_screen1="Game")
        self.texts.setup_H2s(end_screen2="Over")

        self.buttons = Buttons(self.settings, self.screen, retry_button="Retry", quit_button="Quit")

        self.player_sprite = self.settings.sprites["ship_dead4"]

    def draw(self):
        self.texts.draw_text_alignx_center("end_screen1", "H1", 75)
        self.texts.draw_text_alignx_center("end_screen2", "H2", 175)

        sprite = self.player_sprite
        sprite_rect = sprite.get_rect()
        sprite_rect.centerx = self.screen_rect.centerx
        sprite_rect.centery = self.screen_rect.centery
        self.screen.blit(sprite, sprite_rect)

        self.buttons.draw_button_alignx_center("retry_button", 600)
        self.buttons.draw_button_alignx_center("quit_button", 700)


class Texts():
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen

    def setup_H1s(self, **msgs):
        self.H1s = msgs

        for key in self.H1s:
            self.H1s[key] = Text(self.settings, self.screen, self.H1s[key], self.settings.palette.color["text3"], 150)

    def setup_H2s(self, **msgs):
        self.H2s = msgs

        for key in self.H2s:
            self.H2s[key] = Text(self.settings, self.screen, self.H2s[key], self.settings.palette.color["text"], 125)


    def setup_texts(self, **msgs):
        self.texts = msgs

        for key in self.texts:
            self.texts[key] = Text(self.settings, self.screen, self.texts[key], self.settings.palette.color["text"])

    def update_text(self, m, text_type, new_msg):
        if text_type == "H1": self.H1s[m].update_text(new_msg)
        elif text_type == "H2": self.H2s[m].update_text(new_msg)
        elif text_type == "text": self.texts[m].update_text(new_msg)

    def draw_text(self, m, text_type):
        if text_type == "H1": self.H1s[m].draw_text()
        elif text_type == "H2": self.H2s[m].draw_text()
        elif text_type == "text": self.texts[m].draw_text()

    def draw_text_absolute(self, m, text_type, pos):
        if text_type == "H1": self.H1s[m].draw_text_absolute(pos)
        elif text_type == "H2": self.H2s[m].draw_text_absolute(pos)
        elif text_type == "text": self.texts[m].draw_text_absolute(pos)

    def draw_text_alignx_center(self, m, text_type, y):
        if text_type == "H1": self.H1s[m].draw_text_alignx_center(y)
        elif text_type == "H2": self.H2s[m].draw_text_alignx_center(y)
        elif text_type == "text": self.texts[m].draw_text_alignx_center(y)

class Text():

    def __init__(self, settings, screen, msg, color, font_size=48):
        """Initialize text attributes"""
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.text_color = color
        self.font = pygame.font.SysFont(None, font_size)

        self.update_text(msg)

    def update_text(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.settings.palette.color["bg"])
        self.msg_image_rect = self.msg_image.get_rect()

    def draw_text(self):
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def draw_text_absolute(self, pos):
        self.msg_image_rect.centerx = pos[0]
        self.msg_image_rect.centery = pos[1]
        self.draw_text()

    def draw_text_alignx_center(self, y):
        self.msg_image_rect.centerx = self.screen_rect.centerx
        self.msg_image_rect.centery = y
        self.draw_text()
