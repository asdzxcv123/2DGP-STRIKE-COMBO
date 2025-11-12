from pico2d import *

from code import game_framework
from code.state_machine import StateMachine
from sdl2 import *

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 21.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

WALK_SPEED_KMPH = 9.0
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)

JUMP_VELOCITY_MPS = 5.0
JUMP_VELOCITY_PPS = (JUMP_VELOCITY_MPS * PIXEL_PER_METER)


FRAMES_PER_ACTION = 13
TIME_PER_ACTION = 2.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

GRAVITY = 9.8
GRAVITY_PPS = (GRAVITY*PIXEL_PER_METER)

FRICTION_MPS = 4.0
FRICTION_PPS = (FRICTION_MPS * PIXEL_PER_METER)*0.01

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def L_ctrl_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LCTRL

def C_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c


def X_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x

def make_keydown_event(key):
    K = type('K', (), {})()
    K.type = SDL_KEYDOWN
    K.key  = key
    return ('INPUT', K)


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
        self.player.ground_y = self.player.y
        self.player.yv=0
        self.player.move_speed=0
        pass

    def exit(self, e):
        self.player.last_speed=self.player.move_speed
        pass

    def do(self):
        self.player.frame = (self.player.frame + (ACTION_PER_TIME/2)*FRAMES_PER_ACTION*game_framework.frame_time) % self.player.cols
        pass

    def draw(self,camera):
        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        if self.player.face_dir == 1:
            self.player.row_index=0
        else:
            self.player.row_index=1

        screen_x = self.player.x - camera.left
        screen_y = self.player.y - camera.bottom

        self.player.image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                               screen_x, screen_y, 400, 300)




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
        if right_down(e) or left_down(e):
            now = get_time()
            if now - self.keydown_time < 0.5:
                self.player.state_machine.cur_state.exit(e)
                self.player.state_machine.cur_state = self.player.RUN
                self.player.state_machine.cur_state.enter(e)
                self.player.state_machine.next_state = self.player.RUN
            self.keydown_time = now

        self.player.move_speed = WALK_SPEED_PPS

        pass

    def exit(self, e):
        self.player.last_speed = self.player.move_speed
        pass

    def do(self):
        self.player.frame = (self.player.frame + (
                    ACTION_PER_TIME*1.5) * FRAMES_PER_ACTION * game_framework.frame_time) % self.player.cols


        self.player.last_move_speed = self.player.move_speed

        held_right = self.player.key_down_states.get(SDLK_RIGHT, False)
        held_left = self.player.key_down_states.get(SDLK_LEFT, False)
        held_up = self.player.key_down_states.get(SDLK_UP, False)
        held_down = self.player.key_down_states.get(SDLK_DOWN, False)

        x_dir = 0
        if held_right:
            x_dir += 1
            self.player.face_dir = 1
        if held_left:
            x_dir -= 1
            self.player.face_dir = -1
        self.player.x += WALK_SPEED_PPS * game_framework.frame_time * x_dir

        y_dir = 0
        if held_up:
            y_dir += 1
        if held_down:
            y_dir -= 1
        self.player.y += (WALK_SPEED_PPS * 0.7) * game_framework.frame_time * y_dir

        if not (held_right or held_left or held_up or held_down):
            self.player.state_machine.cur_state.exit(None)
            self.player.state_machine.cur_state = self.player.IDLE
            self.player.state_machine.cur_state.enter(None)
        elif (held_up and held_down) and (x_dir == 0):
            self.player.state_machine.cur_state.exit(None)
            self.player.state_machine.cur_state = self.player.IDLE
            self.player.state_machine.cur_state.enter(None)
        pass

    def draw(self,camera):
        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        if  self.player.face_dir==1:
            self.player.row_index=2
        else:
            self.player.row_index=3
        screen_x = self.player.x - camera.left
        screen_y = self.player.y - camera.bottom
        self.player.image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                               screen_x,screen_y, 400, 300)


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

        self.player.move_speed = RUN_SPEED_PPS
        pass

    def exit(self, e):
        self.player.last_speed = self.player.move_speed
        pass

    def do(self):
        self.player.frame = (self.player.frame + (
                    ACTION_PER_TIME*1.3) * FRAMES_PER_ACTION * game_framework.frame_time) % self.player.cols

        held_right = self.player.key_down_states.get(SDLK_RIGHT, False)
        held_left = self.player.key_down_states.get(SDLK_LEFT, False)
        held_up = self.player.key_down_states.get(SDLK_UP, False)
        held_down = self.player.key_down_states.get(SDLK_DOWN, False)
        x_dir = 0
        if held_right:
            x_dir += 1
            self.player.face_dir = 1
        if held_left:
            x_dir -= 1
            self.player.face_dir = -1
        self.player.x += x_dir*RUN_SPEED_PPS*game_framework.frame_time
        y_dir = 0
        if held_up:
            y_dir += 1
        if held_down:
            y_dir -= 1
        self.player.y += (WALK_SPEED_PPS * 0.3) * game_framework.frame_time * y_dir
        self.player.move_speed = RUN_SPEED_PPS
        self.player.last_move_speed = self.player.move_speed


        y_dir = 0
        if self.player.key_down_states.get(SDLK_UP, False):
            y_dir += 1
        if self.player.key_down_states.get(SDLK_DOWN, False):
            y_dir -= 1
        self.player.y += (WALK_SPEED_PPS * 0.4) * game_framework.frame_time * y_dir

        pass

    def draw(self,camera):
        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        if  self.player.face_dir==1:
            self.player.row_index=4
        else:
            self.player.row_index=5
        screen_x = self.player.x - camera.left
        screen_y = self.player.y - camera.bottom
        self.player.image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                               screen_x, screen_y, 400, 300)


        pass

class Jump:
    def __init__(self,Player):
        self.player=Player

        pass
    def enter(self,e):
        self.player.cols=5
        self.player.move_speed=self.player.last_speed
        if self.player.face_dir==1:
            self.player.row_index = 6
        else:
            self.player.row_index = 7

        if self.player.yv==0:
            self.player.yv=JUMP_VELOCITY_PPS
        self.event = None
        pass
    def exit(self,e):
        self.event = None
        pass
    def do(self):
        self.player.frame = (self.player.frame + (
                    ACTION_PER_TIME) * FRAMES_PER_ACTION * game_framework.frame_time) % (self.player.cols-1)
        self.player.yv -= GRAVITY_PPS * game_framework.frame_time
        self.player.y += self.player.yv * game_framework.frame_time

        if self.player.move_speed>0:
            self.player.move_speed -= FRICTION_PPS*game_framework.frame_time

            if self.player.move_speed<0:
                self.player.move_speed=0


        self.player.x += self.player.face_dir*self.player.move_speed*game_framework.frame_time
        if self.player.y <= self.player.ground_y:
            self.player.y = self.player.ground_y
            self.player.yv = 0

            held_right = self.player.key_down_states.get(SDLK_RIGHT, False)
            held_left = self.player.key_down_states.get(SDLK_LEFT, False)
            held_ctrl = self.player.key_down_states.get(SDLK_LCTRL, False)

            self.player.state_machine.cur_state.exit(self.event)

            if held_right ^ held_left:

                self.player.face_dir = 1 if held_right else -1
                self.player.dir = self.player.face_dir

                ev = make_keydown_event(SDLK_RIGHT if held_right else SDLK_LEFT)

                if held_ctrl:
                    self.player.state_machine.cur_state = self.player.RUN
                    self.player.state_machine.cur_state.enter(ev)
                    self.player.state_machine.next_state = self.player.RUN
                else:
                    self.player.state_machine.cur_state = self.player.WALK
                    self.player.state_machine.cur_state.enter(ev)
                    self.player.state_machine.next_state = self.player.WALK
            else:

                self.player.state_machine.cur_state = self.player.IDLE
                self.player.state_machine.cur_state.enter(make_keydown_event(SDLK_RIGHT) if False else self.event)
                self.player.state_machine.next_state = self.player.IDLE

    def draw(self,camera):
        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        if  self.player.face_dir==1:
            self.player.row_index=6
        else:
            self.player.row_index=7
        screen_x = self.player.x - camera.left
        screen_y = self.player.y - camera.bottom

        self.player.image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                               screen_x, screen_y, 400, 300)

        pass

class Attack:
    def __init__(self,Player):
        self.player=Player
        self.next_combo_input_buffered = False
        pass

    def buffer_combo_input(self):
        self.next_combo_input_buffered = True

    def enter(self,e):
        now = get_time()
        self.player.image = self.player.image_attack
        self.player.frame = 0
        self.player.move_speed = 0

        self.player.rows = 10
        self.player.cols=9
        self.player.frame_width = self.player.image.w // self.player.cols
        self.player.frame_height = self.player.image.h // self.player.rows

        self.player.last_attack_time = now

        if now - self.player.last_attack_time < 0.8:
            self.player.combo_stage = (self.player.combo_stage % 4) + 1
        else:
            self.player.combo_stage = 1
        self.next_combo_input_buffered = False

        if self.player.combo_stage == 1:
            self.player.cols = 5
            self.animation_speed_pps = (ACTION_PER_TIME * 2.0) * FRAMES_PER_ACTION
        elif self.player.combo_stage == 2:
            self.player.cols = 5
            self.animation_speed_pps = (ACTION_PER_TIME * 2.0) * FRAMES_PER_ACTION
        elif self.player.combo_stage == 3:
            self.player.cols = 6
            self.animation_speed_pps = (ACTION_PER_TIME * 2.0) * FRAMES_PER_ACTION
        elif self.player.combo_stage == 4:
            self.player.cols = 9
            self.animation_speed_pps = (ACTION_PER_TIME * 2.0) * FRAMES_PER_ACTION
        # elif self.player.combo_stage == 5:
        #     self.player.cols = 8
        #     self.animation_speed_pps = (ACTION_PER_TIME * 2.0) * FRAMES_PER_ACTION


        base_row = (self.player.combo_stage - 1) * 2
        self.player.row_index = base_row
        if self.player.face_dir == 1:
            self.player.row_index = base_row
        else:
            self.player.row_index = base_row + 1



    def exit(self,e):
        self.player.image = self.player.image_motion

        self.player.cols = 13
        self.player.rows = 8
        self.player.frame_width = self.player.image.w // self.player.cols
        self.player.frame_height = self.player.image.h // self.player.rows

        if not self.next_combo_input_buffered:
            self.player.combo_stage = 0
        pass

    def do(self):
        self.player.frame += self.animation_speed_pps * game_framework.frame_time
        if self.player.frame >= self.player.cols:

            if self.next_combo_input_buffered:
                self.player.state_machine.cur_state.exit(None)
                self.player.state_machine.cur_state = self.player.ATTACK
                self.player.state_machine.cur_state.enter(None)

            else:
                self.player.state_machine.cur_state.exit(None)
                self.player.combo_stage = 0
                self.player.state_machine.cur_state = self.player.IDLE
                self.player.state_machine.cur_state.enter(None)
                held_right = self.player.key_down_states.get(SDLK_RIGHT, False)
                held_left = self.player.key_down_states.get(SDLK_LEFT, False)
                held_ctrl = self.player.key_down_states.get(SDLK_LCTRL, False)
                if held_right ^ held_left:

                    self.player.face_dir = 1 if held_right else -1
                    self.player.dir = self.player.face_dir

                    ev = make_keydown_event(SDLK_RIGHT if held_right else SDLK_LEFT)

                    if held_ctrl:
                        self.player.state_machine.cur_state = self.player.RUN
                        self.player.state_machine.cur_state.enter(ev)
                        self.player.state_machine.next_state = self.player.RUN
                    else:
                        self.player.state_machine.cur_state = self.player.WALK
                        self.player.state_machine.cur_state.enter(ev)
                        self.player.state_machine.next_state = self.player.WALK
                else:

                    self.player.state_machine.cur_state = self.player.IDLE
                    self.player.state_machine.cur_state.enter(make_keydown_event(SDLK_RIGHT) if False else None)
                    self.player.state_machine.next_state = self.player.IDLE

        pass

    def draw(self,camera):
        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        base_row = (self.player.combo_stage - 1) * 2

        if self.player.face_dir == 1:
            self.player.row_index = base_row
        else:
            self.player.row_index = base_row + 1

        screen_x = self.player.x - camera.left
        screen_y = self.player.y - camera.bottom
        self.player.image.clip_draw(sx-30, sy, self.player.frame_width, self.player.frame_height,
                                    screen_x, screen_y, 400, 300)

class Run_Attack:
    def __init__(self, Player):
        self.player = Player

    def enter(self,e):
        self.player.image = self.player.image_MtoA
        self.player.frame = 0
        self.player.move_speed = RUN_SPEED_PPS
        self.player.rows = 4
        self.player.cols = 7

        self.animation_speed_pps = (ACTION_PER_TIME * 1.5) * FRAMES_PER_ACTION

        self.player.frame_width = self.player.image.w // self.player.cols
        self.player.frame_height = self.player.image.h // self.player.rows

        if self.player.face_dir == 1:
            self.player.row_index = 0
        else:
            self.player.row_index = 1
        pass


    def exit(self,e):
        self.player.image = self.player.image_motion

        self.player.cols = 13
        self.player.rows = 8
        self.player.frame_width = self.player.image.w // self.player.cols
        self.player.frame_height = self.player.image.h // self.player.rows

        pass

    def do(self):
        self.player.frame += self.animation_speed_pps * game_framework.frame_time
        if self.player.move_speed > 0:
            self.player.move_speed -= FRICTION_PPS * game_framework.frame_time

            if self.player.move_speed < 0:
                self.player.move_speed = 0

        self.player.x += 1.5*self.player.face_dir * self.player.move_speed * game_framework.frame_time


        if self.player.frame >= self.player.cols:
            self.player.state_machine.cur_state.exit(None)


            held_right = self.player.key_down_states.get(SDLK_RIGHT, False)
            held_left = self.player.key_down_states.get(SDLK_LEFT, False)
            held_ctrl = self.player.key_down_states.get(SDLK_LCTRL, False)

            if held_right ^ held_left:
                self.player.face_dir = 1 if held_right else -1
                self.player.dir = self.player.face_dir
                ev = make_keydown_event(SDLK_RIGHT if held_right else SDLK_LEFT)
                if held_ctrl:
                    self.player.state_machine.cur_state = self.player.RUN
                    self.player.state_machine.cur_state.enter(ev)
                    self.player.state_machine.next_state = self.player.RUN
                else:
                    self.player.state_machine.cur_state = self.player.WALK
                    self.player.state_machine.cur_state.enter(ev)
                    self.player.state_machine.next_state = self.player.WALK
            else:
                self.player.state_machine.cur_state = self.player.IDLE
                self.player.state_machine.cur_state.enter(None)
                self.player.state_machine.next_state = self.player.IDLE
        pass

    def draw(self,camera):
        if self.player.face_dir == 1:
            self.player.row_index = 0
        else:
            self.player.row_index = 1

        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        screen_x = self.player.x - camera.left
        screen_y = self.player.y - camera.bottom
        self.player.image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                                    screen_x, screen_y, 400, 300)
        pass

class Jump_Attack:
    def __init__(self, Player):
        self.player = Player

    def enter(self,e):
        self.player.image = self.player.image_MtoA
        self.player.frame = 0

        self.player.rows = 4
        self.player.cols=7

        self.animation_speed_pps = (ACTION_PER_TIME * 1.5) * FRAMES_PER_ACTION
        self.player.frame_width = self.player.image.w // self.player.cols
        self.player.frame_height = self.player.image.h // self.player.rows

        if self.player.face_dir == 1:
            self.player.row_index = 2
        else:
            self.player.row_index = 3

        pass

    def exit(self,e):
        self.player.image = self.player.image_motion

        self.player.cols = 13
        self.player.rows = 8
        self.player.frame_width = self.player.image.w // self.player.cols
        self.player.frame_height = self.player.image.h // self.player.rows

        pass

    def do(self):
        self.player.frame += self.animation_speed_pps * game_framework.frame_time


        self.player.yv -= GRAVITY_PPS * game_framework.frame_time
        self.player.y += self.player.yv * game_framework.frame_time

        if self.player.move_speed > 0:
            self.player.move_speed -= FRICTION_PPS * game_framework.frame_time
            if self.player.move_speed < 0:
                self.player.move_speed = 0
        self.player.x += self.player.face_dir * self.player.move_speed * game_framework.frame_time


        if self.player.y <= self.player.ground_y:
            self.player.y = self.player.ground_y
            self.player.yv = 0


            self.player.state_machine.cur_state.exit(None)

            held_right = self.player.key_down_states.get(SDLK_RIGHT, False)
            held_left = self.player.key_down_states.get(SDLK_LEFT, False)
            held_ctrl = self.player.key_down_states.get(SDLK_LCTRL, False)

            if held_right ^ held_left:
                self.player.face_dir = 1 if held_right else -1
                self.player.dir = self.player.face_dir
                ev = make_keydown_event(SDLK_RIGHT if held_right else SDLK_LEFT)
                if held_ctrl:
                    self.player.state_machine.cur_state = self.player.RUN
                    self.player.state_machine.cur_state.enter(ev)
                    self.player.state_machine.next_state = self.player.RUN
                else:
                    self.player.state_machine.cur_state = self.player.WALK
                    self.player.state_machine.cur_state.enter(ev)
                    self.player.state_machine.next_state = self.player.WALK
            else:
                self.player.state_machine.cur_state = self.player.IDLE
                self.player.state_machine.cur_state.enter(None)
                self.player.state_machine.next_state = self.player.IDLE
            return


        if self.player.frame >= self.player.cols:
            self.player.state_machine.cur_state.exit(None)


            self.player.state_machine.cur_state = self.player.JUMP
            self.player.state_machine.cur_state.enter(None)
        pass

    def draw(self,camera):
        if self.player.face_dir == 1:
            self.player.row_index = 2
        else:
            self.player.row_index = 3

        screen_x = self.player.x - camera.left
        screen_y = self.player.y - camera.bottom

        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height

        self.player.image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                                    screen_x, screen_y, 400, 300)
        pass

class Player:
    Image = None
    def __init__(self):
        self.image_motion = load_image('sprite/player/player_motion.png')
        self.image_attack = load_image('sprite/player/player_attack.png')
        self.image_MtoA=load_image('sprite/player/motion_attack.png')
        self.image = self.image_motion
        self.landing_lock = False  # 착지 직후 이벤트 차단 활성화
        self.wait_neutral = False

        self.x = 400
        self.y = 300
        self.frame = 0
        self.face_dir=1
        self.dir=0
        self.y_dir=0
        self.cols = 13
        self.rows = 8
        self.row_index = 0

        self.last_speed = 0
        self.move_speed = 0
        self.yv = 0
        self.ground_y = self.y
        self.key_down_states={}

        self.combo_stage = 0
        self.last_attack_time = 0.0

        # 프레임 크기 계산
        self.frame_width  = self.image.w // self.cols
        self.frame_height = self.image.h // self.rows

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.ATTACK = Attack(self)
        self.RUN_ATTACK=Run_Attack(self)
        self.JUMP_ATTACK=Jump_Attack(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.WALK, left_down: self.WALK,
                            up_down: self.WALK, down_down:self.WALK,
                            C_down: self.JUMP, X_down: self.ATTACK},
                self.WALK: {L_ctrl_down: self.RUN,C_down: self.JUMP, X_down: self.ATTACK},
                self.RUN: {right_down: self.IDLE, left_down: self.IDLE, right_up: self.IDLE, left_up: self.IDLE,
                           C_down: self.JUMP, X_down: self.RUN_ATTACK},
                self.JUMP:{X_down:self.JUMP_ATTACK},
                self.ATTACK:{},
                self.RUN_ATTACK:{},
                self.JUMP_ATTACK:{},
            }
        )
        self.landing_lock_until = 0.0

    def update(self):
        self.state_machine.update()
        pass

    def draw(self,camera):
        self.state_machine.draw(camera)
        pass

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if self.key_down_states.get(event.key, False):
                return
            self.key_down_states[event.key] = True
        elif event.type == SDL_KEYUP:
            self.key_down_states[event.key] = False

        if self.state_machine.cur_state == self.ATTACK and X_down(('INPUT', event)):
            self.ATTACK.buffer_combo_input()
            return

        if self.landing_lock and event.type in (SDL_KEYDOWN, SDL_KEYUP) and event.key in (SDLK_RIGHT, SDLK_LEFT,
                                                                                          SDLK_LCTRL):
            held_right = self.key_down_states.get(SDLK_RIGHT, False)
            held_left = self.key_down_states.get(SDLK_LEFT, False)
            held_ctrl = self.key_down_states.get(SDLK_LCTRL, False)

            if not self.wait_neutral:

                if not (held_right or held_left or held_ctrl):
                    self.wait_neutral = True
                return


            if event.type == SDL_KEYDOWN:
                self.landing_lock = False
                self.wait_neutral = False
                self.state_machine.handle_state_event(('INPUT', event))
                return
            else:

                return


        self.state_machine.handle_state_event(('INPUT', event))
        pass

