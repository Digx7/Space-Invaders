from Color import ColorPalette
from sprite_manager import *
from Animation import *


class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.fps = 12

        self.palette = ColorPalette(bg=(0, 0, 0),
                                    laser=(255, 0, 0),
                                    text=(255, 255, 255),
                                    text2=(0, 0, 0),
                                    text3=(0, 255, 0),
                                    ui=(0, 255, 0),
                                    player=(255, 255, 255),
                                    cover=(255, 255, 255),
                                    alien1=(0, 255, 0),
                                    alien2=(255, 0, 0),
                                    alien3=(0, 0, 255),
                                    UFO=(0, 255, 0))

        self.bg_color = self.palette.bg_color

        self.sprite_sheet = SpriteSheet('images/SpaceInvadersArt_V2.png')
        self.sprites_raw = {"player_move_anim1": self.sprite_sheet.image_at((0, 0, 16, 16)),
                            "player_move_anim2": self.sprite_sheet.image_at((16, 0, 16, 16)),
                            "player_dead_anim1": self.sprite_sheet.image_at((32, 0, 16, 16)),
                            "player_dead_anim2": self.sprite_sheet.image_at((48, 0, 16, 16)),
                            "player_dead_anim3": self.sprite_sheet.image_at((64, 0, 16, 16)),
                            "player_dead_anim4": self.sprite_sheet.image_at((80, 0, 16, 16)),
                            "cover1": self.sprite_sheet.image_at((0, 16, 16, 16)),
                            "cover2": self.sprite_sheet.image_at((16, 16, 16, 16)),
                            "cover3": self.sprite_sheet.image_at((32, 16, 16, 16)),
                            "cover4": self.sprite_sheet.image_at((48, 16, 16, 16)),
                            "cover5": self.sprite_sheet.image_at((64, 16, 16, 16)),
                            "cover6": self.sprite_sheet.image_at((80, 16, 16, 16)),
                            "alien1_move_anim1": self.sprite_sheet.image_at((0, 32, 16, 16)),
                            "alien1_move_anim2": self.sprite_sheet.image_at((16, 32, 16, 16)),
                            "alien1_dead_anim1": self.sprite_sheet.image_at((32, 32, 16, 16)),
                            "alien1_dead_anim2": self.sprite_sheet.image_at((48, 32, 16, 16)),
                            "alien2_move_anim1": self.sprite_sheet.image_at((0, 48, 16, 16)),
                            "alien2_move_anim2": self.sprite_sheet.image_at((16, 48, 16, 16)),
                            "alien2_dead_anim1": self.sprite_sheet.image_at((32, 48, 16, 16)),
                            "alien2_dead_anim2": self.sprite_sheet.image_at((48, 48, 16, 16)),
                            "alien3_move_anim1": self.sprite_sheet.image_at((0, 64, 16, 16)),
                            "alien3_move_anim2": self.sprite_sheet.image_at((16, 64, 16, 16)),
                            "alien3_dead_anim1": self.sprite_sheet.image_at((32, 64, 16, 16)),
                            "alien3_dead_anim2": self.sprite_sheet.image_at((48, 64, 16, 16)),
                            "ufo_move_anim1": self.sprite_sheet.image_at((0, 80, 16, 16)),
                            "ufo_move_anim2": self.sprite_sheet.image_at((16, 80, 16, 16)),
                            "ufo_dead_anim1": self.sprite_sheet.image_at((32, 80, 16, 16)),
                            "ufo_dead_anim2": self.sprite_sheet.image_at((48, 80, 16, 16)),
                            }

        self.sprite_scale_factor = (64, 64)

        self.sprites = {"ship_move1": self.get_sprite("player_move_anim1", "player"),
                        "ship_move2": self.get_sprite("player_move_anim2", "player"),
                        "ship_dead1": self.get_sprite("player_dead_anim1", "player"),
                        "ship_dead2": self.get_sprite("player_dead_anim2", "player"),
                        "ship_dead3": self.get_sprite("player_dead_anim3", "player"),
                        "ship_dead4": self.get_sprite("player_dead_anim4", "player"),
                        "cover6": self.get_sprite("cover1", "cover"),
                        "cover5": self.get_sprite("cover2", "cover"),
                        "cover4": self.get_sprite("cover3", "cover"),
                        "cover3": self.get_sprite("cover4", "cover"),
                        "cover2": self.get_sprite("cover5", "cover"),
                        "cover1": self.get_sprite("cover6", "cover"),
                        "alien1_move1": self.get_sprite("alien1_move_anim1", "alien1"),
                        "alien1_move2": self.get_sprite("alien1_move_anim2", "alien1"),
                        "alien1_dead1": self.get_sprite("alien1_dead_anim1", "alien1"),
                        "alien1_dead2": self.get_sprite("alien1_dead_anim2", "alien1"),
                        "alien2_move1": self.get_sprite("alien2_move_anim1", "alien2"),
                        "alien2_move2": self.get_sprite("alien2_move_anim2", "alien2"),
                        "alien2_dead1": self.get_sprite("alien2_dead_anim1", "alien2"),
                        "alien2_dead2": self.get_sprite("alien2_dead_anim2", "alien2"),
                        "alien3_move1": self.get_sprite("alien3_move_anim1", "alien3"),
                        "alien3_move2": self.get_sprite("alien3_move_anim2", "alien3"),
                        "alien3_dead1": self.get_sprite("alien3_dead_anim1", "alien3"),
                        "alien3_dead2": self.get_sprite("alien3_dead_anim2", "alien3"),
                        "alien2": self.get_sprite("alien2_move_anim1", "alien2"),
                        "alien3": self.get_sprite("alien3_move_anim1", "alien3"),
                        "ufo_move1": self.get_sprite("ufo_move_anim1", "UFO"),
                        "ufo_move2": self.get_sprite("ufo_move_anim2", "UFO"),
                        "ufo_dead1": self.get_sprite("ufo_dead_anim1", "UFO"),
                        "ufo_dead2": self.get_sprite("ufo_dead_anim2", "UFO"),
                        }

        # Laser settings
        self.laser_width = 10
        self.laser_height = 30
        self.laser_color = self.palette.color["laser"]
        self.lasers_every = 50
        self.alien_lasers_every = 1000

        # Bunker settings
        self.starting_bunker_health = 6
        self.bunker_padding = 50
        self.bunker_height = 600

        # UI settings
        self.total_lives = 3
        self.alien1_points = 50
        self.alien2_points = 100
        self.alien3_points = 1000
        self.ufo_points = 10000
        self.score_scale = 1.5

        # Scene settings
        self.scenes = {"menu": "_menu",
                       "main": "_main",
                       "end": "_end"}

        self.initialize_speed_settings()

        self.ufo_odds = 1

    def initialize_speed_settings(self):
        self.ship_speed_factor = 1

        self.laser_speed_factor = 1
        self.alien_laser_speed_factor = -0.25

        self.alien_left_right_speed_factor = 0.5
        self.ufo_speed_factor = 0.75
        self.alien_drop_speed_factor = 5
        # alien_move_direction: 1 = right; -1 = left

        self.alien_move_direction = 1

        self.speedup_scale = 1.1

    def increase_speed(self):
        scale = self.speedup_scale
        self.ship_speed_factor *= scale
        self.laser_speed_factor *= scale

        self.alien_left_right_speed_factor *= scale

        self.alien1_points = int(self.alien1_points * self.score_scale)
        self.alien2_points = int(self.alien2_points * self.score_scale)
        self.alien3_points = int(self.alien3_points * self.score_scale)
        self.ufo_points = int(self.ufo_points * self.score_scale)

    def reset_speed(self):
        self.initialize_speed_settings()

    def get_sprite(self, raw_sprite, color):
        output_sprite = self.sprites_raw[raw_sprite]
        output_sprite.fill(self.palette.color[color], special_flags=pygame.BLEND_MULT)
        output_sprite = pygame.transform.scale(output_sprite, self.sprite_scale_factor)
        output_sprite.set_colorkey(self.palette.color["bg"])
        return output_sprite
