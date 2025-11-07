from pico2d import *
from code.state_machine import StateMachine
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_LCTRL
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def L_ctrl_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LCTRL

class Idle:
    def __init__(self, Player):
        self.player = Player
        pass

    def enter(self, e):
        if self.player.face_dir==-1:
            self.player.row_index = 1
        else:
            self.player.row_index = 0
        self.player.cols=13
        self.dir=0
        pass

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % self.player.cols
        pass

    def draw(self):
        sx = self.player.frame * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        if self.player.face_dir == 1:
            self.player.row_index=0
        else:
            self.player.row_index=1
        Player.Image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                               self.player.x, self.player.y, 400, 300)


        delay(0.2)

class Walk:
    def __init__(self, Player):
        self.player = Player
        self.keydown_time = 0
        pass

    def enter(self, e):
        if self.player.face_dir==1:
            self.player.row_index = 2
        else:
            self.player.row_index = 3
        self.player.cols=10
        if right_down(e) or left_up(e):
            self.player.dir = self.player.face_dir = 1
        elif left_down(e) or right_up(e):
            self.player.dir = self.player.face_dir = -1
        now = get_time()
        if now - self.keydown_time < 0.5:
            self.player.state_machine.cur_state.exit(e)
            self.player.state_machine.cur_state = self.player.RUN
            self.player.state_machine.cur_state.enter(e)
            self.player.state_machine.next_state = self.player.RUN
        self.keydown_time = now
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
        if  self.player.face_dir==1:
            self.player.row_index=2
        else:
            self.player.row_index=3
        Player.Image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                               self.player.x, self.player.y, 400, 300)
        delay(0.05)

class RUN:
    def __init__(self, Player):
        self.player = Player
        pass

    def enter(self, e):
        if self.player.face_dir==1:
            self.player.row_index = 4
        else:
            self.player.row_index = 5
        self.player.cols=7

        pass

    def exit(self, e):

        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % self.player.cols
        self.player.x += self.player.face_dir * 10


        pass

    def draw(self):
        sx = self.player.frame * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        if  self.player.face_dir==1:
            self.player.row_index=4
        else:
            self.player.row_index=5
        Player.Image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                               self.player.x, self.player.y, 400, 300)
        delay(0.03)

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
        self.dir=0
        self.cols = 13
        self.rows = 8
        self.row_index = 0

        # 프레임 크기 계산
        self.frame_width  = Player.Image.w // self.cols
        self.frame_height = Player.Image.h // self.rows

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.RUN = RUN(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.WALK, left_down: self.WALK, right_up: self.WALK, left_up: self.WALK },
                self.WALK: {right_down: self.IDLE, left_down: self.IDLE, right_up: self.IDLE, left_up: self.IDLE, L_ctrl_down: self.RUN},
                self.RUN: {right_down: self.IDLE, left_down: self.IDLE, right_up: self.IDLE, left_up: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()
        pass

    def draw(self):
        self.state_machine.draw()
        pass

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))
        pass
