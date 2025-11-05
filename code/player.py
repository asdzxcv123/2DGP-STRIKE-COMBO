from pico2d import *

class Player:
    Image = None
    def __init__(self):

        if Player.Image == None:
            Player.Image = load_image('sprite/player/player_motion.png')

        self.x = 400
        self.y = 300
        self.frame = 0

        self.cols = 13
        self.rows = 4
        self.row_index = 0

        # 프레임 크기 계산
        self.frame_width  = Player.Image.w // self.cols
        self.frame_height = Player.Image.h // self.rows

    def update(self):
        # 첫 번째 줄만 순환
        self.frame = (self.frame + 1) % self.cols

    def draw(self):

        sx = self.frame * self.frame_width
        sy = (self.rows - 1 - self.row_index) * self.frame_height

        Player.Image.clip_draw(
            sx, sy,
            self.frame_width, self.frame_height,
            self.x, self.y
        )
        delay(0.5)

    def handle_event(self, event):
        pass
