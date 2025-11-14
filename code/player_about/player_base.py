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

def H_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_h

def make_keydown_event(key):
    K = type('K', (), {})()
    K.type = SDL_KEYDOWN
    K.key  = key
    return ('INPUT', K)

def add_afterimage(player, image):
    player.afterimages.append({
        'x': player.x,
        'z': player.z, # y -> z
        'y': player.y, # 높이 추가
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
        screen_y = (a['z'] + a['y']) - camera.bottom # (z-y) 적용

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

def check_collision_3d(hitbox, hurtbox):
    x1_hit, y1_hit, z1_hit, x2_hit, y2_hit, z2_hit = hitbox #히트박스 튜플
    x1_hurt, y1_hurt, z1_hurt, x2_hurt, y2_hurt, z2_hurt = hurtbox# 허트박스 튜플

    # X축, Y축, Z축 모두에서 겹치는지 확인
    x_overlap = (x1_hit < x2_hurt) and (x2_hit > x1_hurt)
    y_overlap = (y1_hit < y2_hurt) and (y2_hit > y1_hurt)
    z_overlap = (z1_hit < z2_hurt) and (z2_hit > z1_hurt)

    return x_overlap and y_overlap and z_overlap


def draw_3d_box(owner, box, camera):
    x1, y1, z1, x2, y2, z2 = box

    # --- 1. 지면 사각형 (X, Z) ---
    # 박스의 맨 아래 높이(y1)를 기준으로 너비(x)와 깊이(z)를 그립니다.
    # '발밑 영역'을 확인하기 좋습니다.

    # 지면 투영 (후면-좌측, 전면-우측)
    g_sx1 = x1 - camera.left
    g_sy1 = (z1 + y1) - camera.bottom  # 후면 (z1)

    g_sx2 = x2 - camera.left
    g_sy2 = (z2 + y1) - camera.bottom  # 전면 (z2)

    # draw_rectangle은 (왼쪽, 아래, 오른쪽, 위) 좌표를 받습니다.
    # z 값이 클수록 화면상 y가 높아지는 것을 감안하여 min, max를 사용합니다.
    draw_rectangle(int(g_sx1), int(min(g_sy1, g_sy2)),
                   int(g_sx2), int(max(g_sy1, g_sy2)))

    # --- 2. 높이 사각형 (X, Y) ---
    # 박스의 Z축 중심을 기준으로 너비(x)와 높이(y)를 그립니다.
    # '공격 높이'나 '피격 높이'를 확인하기 좋습니다.

    # Z축 중심 계산
    #cz = (z1 + z2) / 2
    cz=owner.z
    # 높이 투영 (중심깊이-하단-좌측, 중심깊이-상단-우측)
    h_sx1 = x1 - camera.left
    h_sy1 = (cz + y1) - camera.bottom  # 하단 (y1)

    h_sx2 = x2 - camera.left
    h_sy2 = (cz + y2) - camera.bottom  # 상단 (y2)

    draw_rectangle(int(h_sx1), int(h_sy1), int(h_sx2), int(h_sy2))