from pico2d import *
from code import game_framework
from code import game_world
from code.player_about.player_base import *


class DashEffect:
    image = None

    def __init__(self, x, z, y, face_dir): # x, y -> x, z, y
        self.x, self.z, self.y = x, z, y # z, y 적용
        self.face_dir = face_dir
        self.frame = 0.0
        self.cols=5
        self.rows=2
        self.row_index=0

        if DashEffect.image == None:
            DashEffect.image = load_image('sprite/skill/Dash_effect.png')


        self.frame_width = self.image.w // self.cols
        self.frame_height = self.image.h // self.rows
        self.animation_speed_pps = (ACTION_PER_TIME * 3.0) * FRAMES_PER_ACTION

    def update(self):
        self.frame += self.animation_speed_pps * game_framework.frame_time
        if self.frame > self.cols:
            game_world.remove_object(self)
        pass
    def draw(self, camera):

        if self.face_dir == 1:
            self.row_index = 0
        else:
            self.row_index = 1
        screen_x = self.x - camera.left
        screen_y = (self.z + self.y) - camera.bottom # (z-y) 적용

        sx = int(self.frame) * self.frame_width
        sy = (self.rows - 1 - self.row_index) * self.frame_height

        self.image.clip_draw(sx, sy, self.frame_width, self.frame_height,
                                    screen_x, screen_y, 1000, 1000)