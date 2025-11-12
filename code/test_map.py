from pico2d import *

class Test_Road:
    def __init__(self):
        self.image = load_image('sprite/map/test_road.png')

    def update(self):
        pass

    def draw(self,camera):
        self.image.draw(400, 30)


