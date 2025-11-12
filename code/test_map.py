from pico2d import *

class Test_Road:
    def __init__(self):
        self.image = load_image('sprite/map/test_road.png')
        # 맵 크기를 이미지 크기에 맞춰 고정
        self.w = self.image.w
        self.h = self.image.h

    def update(self):
        pass

    def draw(self, camera):
        sx = int(camera.left)

        # 화면 크기에 맞춰 자를 높이
        sh = int(min(camera.canvas_height, self.h))
        sw = int(min(camera.canvas_width, self.w - sx))

        # 시작 y를 '밑에서부터' 계산
        sy = self.h - sh

        if sx < 0:
            sx = 0
        if sx + sw > self.w:
            sw = self.w - sx
        if sw <= 0 or sh <= 0:
            return

        # 자른 부분을 화면 하단(0,0)에 붙이기
        self.image.clip_draw(sx, sy, sw+200, sh, 500, 300)
