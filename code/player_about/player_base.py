from sdl2 import *
from pico2d import *
from code import game_framework, game_world
from code.player_skill.bash_projectil import SwordP
from code.state_machine import StateMachine
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

AFTERIMAGE_DURATION_SEC = 0.2

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

def Q_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_q

def Shift_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LSHIFT

def make_keydown_event(key):
    K = type('K', (), {})()
    K.type = SDL_KEYDOWN
    K.key  = key
    return ('INPUT', K)

def add_afterimage(player, image):
    player.afterimages.append({
        'x': player.x,
        'y': player.y,
        'frame': player.frame,
        'row_index': player.row_index,
        'frame_width': player.frame_width,
        'frame_height': player.frame_height,
        'rows': player.rows,
        'cols': player.cols,
        'image': image,
        'dur_time': 0
    })

def update_afterimages(player, dt):
    new_list = []
    for a in player.afterimages:
        a['dur_time'] += dt
        if a['dur_time'] < AFTERIMAGE_DURATION_SEC:
            new_list.append(a)
    player.afterimages = new_list
    pass


def draw_afterimages(player,camera):
    for a in player.afterimages:
        t=a['dur_time']/AFTERIMAGE_DURATION_SEC
        alpha = max(0.0, 1.0 - t)

        a['image'].opacify(alpha)

        screen_x = a['x'] - camera.left
        screen_y = a['y'] - camera.bottom

        sx = int(a['frame']) * a['frame_width']
        sy = (a['rows'] - 1 - a['row_index']) * a['frame_height']

        a['image'].clip_draw(sx, sy, a['frame_width'], a['frame_height'],
                             screen_x, screen_y, 400, 300)


    if player.afterimages:
        player.image_motion.opacify(1.0)
        player.image_attack.opacify(1.0)
        player.image_MtoA.opacify(1.0)
        player.image_bash.opacify(1.0)
        player.image_dash.opacify(1.0)
    pass