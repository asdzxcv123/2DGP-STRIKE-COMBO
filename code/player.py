from pico2d import *

from code import game_framework
from code.state_machine import StateMachine
from sdl2 import *

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

WALK_SPEED_KMPH = 7.0
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)

JUMP_SPEED_KMPH = 2.0
JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

FRAMES_PER_ACTION = 13
TIME_PER_ACTION = 2.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


GRAVITY = 9.8




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

def C_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c

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
        self.player.frame = (self.player.frame + (ACTION_PER_TIME/2)*FRAMES_PER_ACTION*game_framework.frame_time) % self.player.cols
        pass

    def draw(self):
        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        if self.player.face_dir == 1:
            self.player.row_index=0
        else:
            self.player.row_index=1
        Player.Image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                               self.player.x, self.player.y, 400, 300)




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
        self.player.frame = (self.player.frame + (
                    ACTION_PER_TIME*1.5) * FRAMES_PER_ACTION * game_framework.frame_time) % self.player.cols

        self.player.x += WALK_SPEED_PPS*game_framework.frame_time*self.player.face_dir
        pass

    def draw(self):
        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        if  self.player.face_dir==1:
            self.player.row_index=2
        else:
            self.player.row_index=3
        Player.Image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                               self.player.x, self.player.y, 400, 300)


class Run:
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
        self.player.frame = (self.player.frame + (
                    ACTION_PER_TIME*1.3) * FRAMES_PER_ACTION * game_framework.frame_time) % self.player.cols

        self.player.x += self.player.face_dir*RUN_SPEED_PPS*game_framework.frame_time


        pass

    def draw(self):
        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        if  self.player.face_dir==1:
            self.player.row_index=4
        else:
            self.player.row_index=5
        Player.Image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                               self.player.x, self.player.y, 400, 300)


        pass

class Jump:
    def __init__(self,Player):
        self.player=Player
        pass
    def enter(self,e):
        self.player.cols=5
        if self.player.face_dir==1:
            self.player.row_index = 6
        else:
            self.player.row_index = 7
        pass
    def exit(self,e):

        pass
    def do(self):
        self.player.frame = (self.player.frame + (
                    ACTION_PER_TIME) * FRAMES_PER_ACTION * game_framework.frame_time) % self.player.cols

        pass
    def draw(self):
        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        if  self.player.face_dir==1:
            self.player.row_index=6
        else:
            self.player.row_index=7

        Player.Image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                               self.player.x, self.player.y, 400, 300)

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
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.WALK, left_down: self.WALK, right_up: self.WALK, left_up: self.WALK, C_down: self.JUMP},
                self.WALK: {right_down: self.IDLE, left_down: self.IDLE, right_up: self.IDLE, left_up: self.IDLE, L_ctrl_down: self.RUN, C_down: self.JUMP},
                self.RUN: {right_down: self.IDLE, left_down: self.IDLE, right_up: self.IDLE, left_up: self.IDLE, C_down: self.JUMP},
                self.JUMP:{}
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
