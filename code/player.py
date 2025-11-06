from pico2d import *
from code.state_machine import StateMachine

def right_down(e):
    pass

def right_up(e):
    pass

def left_down(e):
    pass

def left_up(e):
    pass


class Idle:
    def __init__(self, Player):
        self.player = Player
        pass

    def enter(self, e):

        pass

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % self.player.cols
        pass

    def draw(self):
        sx = self.player.frame * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height

        Player.Image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height + 30,
                               self.player.x, self.player.y, 400, 300)
        delay(0.2)
        pass
class Walk:
    def __init__(self, Player):
        self.player = Player

        pass

    def enter(self, e):
        self.player.row_index = 3
        self.player.cols=10
        pass

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % self.player.cols
        self.player.x += self.player.face_dir * 5
        pass

    def draw(self):
        sx = self.player.frame * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height

        Player.Image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                               self.player.x, self.player.y, 400, 300)
        delay(0.2)
        pass
class Player:
    Image = None
    def __init__(self):

        if Player.Image == None:
            Player.Image = load_image('sprite/player/player_motion.png')

        self.x = 400
        self.y = 300
        self.frame = 0
        self.face_dir=1

        self.cols = 13
        self.rows = 4
        self.row_index = 0

        # 프레임 크기 계산
        self.frame_width  = Player.Image.w // self.cols
        self.frame_height = Player.Image.h // self.rows

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.state_machine = StateMachine(
            self.WALK,
            {
                self.IDLE: { },
            }
        )

    def update(self):
        self.state_machine.update()
        pass

    def draw(self):
        self.state_machine.draw()
        pass

    def handle_event(self, event):
        #self.state_machine.handle_event(event)
        pass
