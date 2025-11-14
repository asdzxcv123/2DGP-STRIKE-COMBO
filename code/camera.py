from pico2d import *

class Camera:
    def __init__(self,canvas_width, canvas_height):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.left = 0
        self.bottom = 0

        self.world_width = 0
        self.world_height = 0
        pass

    def world_size(self,width, height):
        self.world_width = width
        self.world_height = height
        pass

    def update(self, target):
        self.left = target.x - (self.canvas_width // 2)
        # target.y -> target.z (깊이 축을 따라감)
        self.bottom = target.z - (self.canvas_height // 2)

        self.left = clamp(0, self.left, self.world_width - self.canvas_width)
        self.bottom = clamp(0, self.bottom, self.world_height - self.canvas_height)
        pass