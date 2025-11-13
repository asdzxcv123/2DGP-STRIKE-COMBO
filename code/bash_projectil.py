from pico2d import *
import code.game_framework
import code.game_world

PIXEL_PER_METER = (10.0 / 0.3)
PROJ_SPEED_KMPH = 42.0

class SwordP:
    image = None
    def __init__(self):
        if SwordP==None:
            SwordP.image=load_image('sprite/skill/bash_proj.png')
    pass

    def draw(self):

        pass

    def update(self):

        pass
