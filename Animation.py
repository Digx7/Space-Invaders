import pygame


class Animations():
    def __init__(self, **animations):
        self.animations = animations
        self.current_key = "idle"
        self.current_animation = self.animations[self.current_key]

    def set_current_animation(self, key):
        self.current_animation.current_index = 0

        self.current_key = key
        self.current_animation = self.animations[self.current_key]

    def get_current_animation(self):
        return self.current_animation

    def check_if_fin(self):
        return self.current_animation.check_if_at_end()


class Animation():
    def __init__(self, frames, max_loops=0):
        self.frames = frames
        self.max_loops = max_loops
        self.current_loop = 0
        self.current_index = 0
        self.current_frame = self.frames[self.current_index]

    def update(self):
        self.increment_frame()
        return self.get_current_frame()

    def increment_frame(self):
        self.current_index += 1
        if self.current_index >= len(self.frames) and self.max_loops == 0:
            self.current_index = 0
        elif self.current_index >= len(self.frames) and self.max_loops > 0:
            self.current_loop += 1
            if self.current_loop >= self.max_loops: self.current_index -= 1
            else: self.current_index = 0

    def get_current_frame(self):
        self.current_frame = self.frames[self.current_index]
        return self.current_frame

    def check_if_at_end(self):
        if self.current_loop >= self.max_loops:
            return True
        else:
            return False
