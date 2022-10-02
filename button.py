import pygame.font


class Buttons():
    def __init__(self, settings, screen, **msgs):
        self.settings = settings
        self.screen = screen
        self.msgs = msgs

        self.setup_buttons()

    def setup_buttons(self):
        for key in self.msgs:
            self.msgs[key] = Button(self.settings, self.screen, self.msgs[key])

    def draw_button(self, m):
        self.msgs[m].draw_button()

    def draw_button_absolute(self, m, pos):
        self.msgs[m].draw_button_absolute(pos)

    def draw_button_alignx_center(self, m, y):
        self.msgs[m].draw_button_alignx_center(y)

    def check_button(self, key, mouse_x, mouse_y):
        return self.msgs[key].check_button(mouse_x, mouse_y)


class Button():

    def __init__(self, settings, screen, msg):
        """Initialize button attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimiensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = settings.palette.color["ui"]
        self.text_color = settings.palette.color["text2"]
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message"""
        self.msg_image_rect.center = self.rect.center
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def draw_button_absolute(self, pos):
        """Sets the exact position of the button, then draws it"""
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.draw_button()

    def draw_button_alignx_center(self, y):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = y
        self.draw_button()


    def check_button(self, mouse_x, mouse_y):
        """Check to see if the mouse is over the button"""
        if self.rect.collidepoint(mouse_x, mouse_y):
            return True
