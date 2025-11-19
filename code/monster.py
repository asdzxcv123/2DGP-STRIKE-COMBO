from pico2d import *
import random
import math

from code import game_framework, game_world
from code.player_about.player_base import *  # 상수 및 함수 활용
from code.state_machine import StateMachine


# 몬스터 AI 상태 이벤트
def anim_end(e): return e[0] == 'ANIM_END'


def see_player(e): return e[0] == 'AI_DECISION' and e[1] == 'CHASE'


def attack_range(e): return e[0] == 'AI_DECISION' and e[1] == 'ATTACK'


class MonsterState:
    def __init__(self, monster):
        self.monster = monster

    def enter(self, event):
        pass

    def do(self):
        pass

    def exit(self, event):
        pass

    def draw(self, camera):
        sx = int(self.monster.frame) * self.monster.frame_width
        sy = 0
        screen_x = self.monster.x - camera.left
        screen_y = (self.monster.z + self.monster.y) - camera.bottom

        if self.monster.face_dir == 1:  # 오른쪽
            self.monster.image.clip_draw(sx, sy, self.monster.frame_width, self.monster.frame_height, screen_x,
                                         screen_y,200,200)
        else:  # 왼쪽
            self.monster.image.clip_composite_draw(sx, sy, self.monster.frame_width, self.monster.frame_height,
                                                   0,'h', screen_x, screen_y,200,200)


# --- 상태 구현 ---
class M_Idle(MonsterState):
    def enter(self, event):
        self.monster.image = self.monster.image_walk
        self.monster.frame = 0
        self.monster.cols = 4
        self.monster.frame_width = self.monster.image.w // self.monster.cols
        self.monster.frame_height = self.monster.image.h
        self.timer = 0

    def do(self):
        self.monster.frame = (self.monster.frame + 8.0 * game_framework.frame_time) % self.monster.cols
        self.timer += game_framework.frame_time
        if self.timer > 1.0:  # 1초마다 행동 결정 (추적 로직 등 추가 가능)
            pass


class M_Walk(MonsterState):  # 플레이어 추적 등 구현 가능
    pass


class M_Attack(MonsterState):
    def enter(self, event):
        self.monster.image = self.monster.image_attack
        self.monster.frame = 0
        self.monster.cols = 5
        self.monster.frame_width = self.monster.image.w // self.monster.cols
        self.monster.frame_height = self.monster.image.h
        self.attack_checked = False

    def do(self):
        self.monster.frame += 10.0 * game_framework.frame_time
        if int(self.monster.frame) >= 2 and not self.attack_checked:
            self.attack_checked = True
            # 여기서 공격 히트박스를 생성하거나 play_mode에서 처리

        if self.monster.frame >= self.monster.cols:
            self.monster.state_machine.handle_state_event(('ANIM_END', 0))


class M_Die(MonsterState):
    def enter(self, event):
        self.monster.image = self.monster.image_die
        self.monster.frame = 0
        self.monster.cols = 5
        self.monster.frame_width = self.monster.image.w // self.monster.cols
        self.monster.frame_height = self.monster.image.h

    def do(self):
        if self.monster.frame < self.monster.cols - 1:
            self.monster.frame += 8.0 * game_framework.frame_time
        else:
            game_world.remove_object(self.monster)


# --- 몬스터 메인 클래스 ---
class Monster:
    def __init__(self, x, z):

        self.x, self.z, self.y = x, z, 0
        self.hp = 50
        self.face_dir = -1

        # 이미지 로드 (업로드된 파일명 기준)
        self.image_walk = load_image('sprite/monster/monster_walk.png')
        self.image_attack = load_image('sprite/monster/monster_attack.png')
        self.image_die = load_image('sprite/monster/monster_die.png')
        self.image = self.image_walk

        # 히트박스 설정
        self.hurt_w, self.hurt_h, self.hurt_d = 60, 120, 30
        self.hurt_offset_x, self.hurt_offset_y = 0, 0
        self.hurt_offset_z = -40
        # 상태 머신
        self.IDLE = M_Idle(self)
        self.ATTACK = M_Attack(self)
        self.DIE = M_Die(self)
        self.state_machine = StateMachine(self.IDLE, {
            self.IDLE: {attack_range: self.ATTACK},
            self.ATTACK: {anim_end: self.IDLE},
            self.DIE: {}
        })

        # 초기 프레임 설정
        self.frame = 0
        self.cols = 4
        self.rows = 1
        self.frame_width = self.image_walk.w // 4
        self.frame_height = self.image_walk.h

    def get_bb_3d(self):
        cx = self.x + self.hurt_offset_x
        cy = self.y + self.hurt_offset_y
        cz = self.z + self.hurt_offset_z

        half_w = self.hurt_w / 2
        half_d = self.hurt_d / 2

        x1 = cx - half_w
        x2 = cx + half_w
        y1 = cy
        y2 = cy + self.hurt_h  # y1(바닥) 부터 y2(머리) 까지
        z1 = cz - half_d
        z2 = cz + half_d

        return (x1, y1, z1, x2, y2, z2)

    def on_hit(self, damage):
        print(f"Monster Hit! HP: {self.hp} -> {self.hp - damage}")
        self.hp -= damage
        if self.hp <= 0:
            self.state_machine.cur_state = self.DIE
            self.DIE.enter(None)

    def update(self):
        self.state_machine.update()

    def draw(self, camera):
        self.state_machine.draw(camera)
        # 디버그용 박스 (필요시 주석 해제)
        draw_3d_box(self, self.get_bb_3d(), camera)