from pico2d import *
from code import game_framework
from code import game_world
PIXEL_PER_METER = (10.0 / 0.3)
PROJ_SPEED_KMPH = 42.0
PROJ_SPEED_MPM = (PROJ_SPEED_KMPH * 1000.0 / 60.0)
PROJ_SPEED_MPS = (PROJ_SPEED_MPM / 60.0)
PROJ_SPEED_PPS = (PROJ_SPEED_MPS * PIXEL_PER_METER)
class SwordP:
    image = None
    def __init__(self,x,z,y,face_dir): # x, y -> x, z, y
        self.x, self.z, self.y = x, z, y # z, y 적용
        if SwordP.image==None:
            SwordP.image=load_image('sprite/skill/bash_proj.png')
        self.dir=face_dir
        self.st_x, self.st_z=x, z # st_y -> st_z

        pass

    def draw(self,camera):
        screen_x = self.x - camera.left
        screen_y = (self.z - self.y) - camera.bottom # (z-y) 적용
        if self.dir==1:
            SwordP.image.composite_draw(0, 'h', screen_x, screen_y, 200, 300)
        else:
            SwordP.image.draw(screen_x, screen_y, 200, 300)
        pass

    def update(self):
        self.x+=PROJ_SPEED_PPS * self.dir * game_framework.frame_time
        # 투사체는 z, y축(깊이, 높이)으로는 움직이지 않음
        if self.dir==1:
            if self.x>self.st_x+800:
                game_world.remove_object(self)
        else:
            if self.x < self.st_x-800:
                game_world.remove_object(self)


        pass