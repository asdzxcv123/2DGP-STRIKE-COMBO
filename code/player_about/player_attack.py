from code.player_about.player_base import *


class Attack:
    def __init__(self,Player):
        self.player=Player
        self.next_combo_input_buffered = False
        # (offset_x, offset_z, width, height, depth)
        self.hitbox_data = { }

        pass

    def buffer_combo_input(self):
        self.next_combo_input_buffered = True

    def enter(self,e):
        self.player.hit_list=[]
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
            self.player.combo_stage = (self.player.combo_stage % 5) + 1
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
            self.player.cols = 5
            self.animation_speed_pps = (ACTION_PER_TIME * 2.0) * FRAMES_PER_ACTION
        elif self.player.combo_stage == 5:
             self.player.cols = 8
             self.player.frame=5
             self.animation_speed_pps = (ACTION_PER_TIME * 2.0) * FRAMES_PER_ACTION

        if  self.player.combo_stage<4:
            base_row = (self.player.combo_stage - 1) * 2
        else:
            base_row = (4 - 1) * 2
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
        self.player.active_hitbox = None
        pass

    def do(self):
        # 공격 중에는 y(높이)가 0으로 고정 (공중 공격이 아니므로)
        if self.player.face_dir == 1:
            self.player.hurt_offset_x = 5
        else:
            self.player.hurt_offset_x = -30
        attack_offset_x=40
        #offset조정은 150기준 40, 증가할떄 증가 혹은 감소값의 1/2을더하면됨
        if self.player.face_dir == 1:
            self.hitbox_data = {
                1: (self.player.hurt_offset_x+attack_offset_x, 0, 150, 150, 30),  # 1타 (앞으로 50, 폭 80, 높이 80, 깊이 30)
                2: (self.player.hurt_offset_x+attack_offset_x, 0, 150, 150, 30),  # 2타
                3: (self.player.hurt_offset_x+attack_offset_x+10, 0, 170, 130, 50),  # 3타 (더 길고 넓게)
                4: (self.player.hurt_offset_x+attack_offset_x+15, 0, 180, 100, 70),  # 4타
                5: (self.player.hurt_offset_x+attack_offset_x-15, 0, 120, 170, 40)  # 5타 (막타)
            }
        else:
            self.hitbox_data = {
                1: (-self.player.hurt_offset_x + attack_offset_x, 0, 150, 150, 30),  # 1타 (앞으로 50, 폭 80, 높이 80, 깊이 30)
                2: (-self.player.hurt_offset_x + attack_offset_x, 0, 150, 150, 30),  # 2타
                3: (-self.player.hurt_offset_x + attack_offset_x + 10, 0, 170, 130, 50),  # 3타 (더 길고 넓게)
                4: (-self.player.hurt_offset_x + attack_offset_x + 15, 0, 180, 100, 70),  # 4타
                5: (-self.player.hurt_offset_x + attack_offset_x - 15, 0, 120, 170, 40)  # 5타 (막타)
            }
        self.player.y = 0
        self.player.yv = 0

        self.player.frame += self.animation_speed_pps * game_framework.frame_time

        data = self.hitbox_data.get(self.player.combo_stage)

        # (임시) 공격 애니메이션의 특정 프레임에서만 활성화 (2프레임 ~ 끝-2프레임)
        # 이 프레임 범위는 나중에 직접 조정하셔야 합니다.
        if data and (self.player.frame >= 0.0 and self.player.frame < self.player.cols):
            offset_x_rel, offset_z, width, height, depth = data

            # 1. 방향에 맞게 x 오프셋 적용
            offset_x = offset_x_rel * self.player.face_dir

            # 2. 히트박스 중심 좌표 계산
            cx = self.player.x + offset_x
            cy = self.player.y-100  # y 오프셋은 0 (바닥부터)
            cz = self.player.z + offset_z

            # 3. 최종 좌표 (x1, y1, z1, x2, y2, z2) 계산
            half_w = width / 2
            half_d = depth / 2

            x1 = cx - half_w
            x2 = cx + half_w
            y1 = cy  # (player.y)부터
            y2 = cy + height  # (player.y + height)까지
            z1 = cz - half_d
            z2 = cz + half_d

            self.player.active_hitbox = (x1, y1, z1, x2, y2, z2)
        else:

            self.player.active_hitbox = None


        if self.player.frame >= self.player.cols:
            self.player.active_hitbox = None
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
        # [수정] (z - y) -> (z + y)
        screen_y = (self.player.z + self.player.y) - camera.bottom
        self.player.image.clip_draw(sx-30, sy, self.player.frame_width, self.player.frame_height,
                                    screen_x, screen_y, 400, 300)
class Run_Attack:
    def __init__(self, Player):
        self.hitbox_data =()
        self.player = Player

    def enter(self,e):
        self.player.image = self.player.image_MtoA
        self.player.frame = 0
        self.player.move_speed = RUN_SPEED_PPS
        self.player.rows = 4
        self.player.cols = 7
        self.player.hit_list = []
        self.animation_speed_pps = (ACTION_PER_TIME * 1.5) * FRAMES_PER_ACTION

        self.player.frame_width = self.player.image.w // self.player.cols
        self.player.frame_height = self.player.image.h // self.player.rows

        if self.player.face_dir == 1:
            self.player.row_index = 0
        else:
            self.player.row_index = 1
        pass

        if self.player.face_dir == 1:
            self.player.hurt_offset_x = -55
        else:
            self.player.hurt_offset_x = -75


    def exit(self,e):
        self.player.image = self.player.image_motion

        self.player.cols = 13
        self.player.rows = 8
        self.player.frame_width = self.player.image.w // self.player.cols
        self.player.frame_height = self.player.image.h // self.player.rows
        self.player.active_hitbox = None
        pass

    def do(self):
        # 달리는 공격이므로 y(높이)는 0
        self.player.y = 0
        self.player.yv = 0

        self.player.frame += self.animation_speed_pps * game_framework.frame_time
        if self.player.move_speed > 0:
            self.player.move_speed -= FRICTION_PPS * game_framework.frame_time

            if self.player.move_speed < 0:
                self.player.move_speed = 0

        self.player.x += 1.5*self.player.face_dir * self.player.move_speed * game_framework.frame_time

        if self.player.face_dir==1:
            self.hitbox_data = (self.player.hurt_offset_x, 0, 300, 100, 40)
        else:
            self.hitbox_data = (-self.player.hurt_offset_x, 0, 300, 100, 40)

        data = self.hitbox_data
        if data and (self.player.frame > 2.0 and self.player.frame < self.player.cols - 2.0):
            offset_x_rel, offset_z, width, height, depth = data
            offset_x = offset_x_rel * self.player.face_dir

            cx = self.player.x + offset_x
            cy = self.player.y - 100
            cz = self.player.z + offset_z
            half_w, half_d = width / 2, depth / 2

            x1, x2 = cx - half_w, cx + half_w
            y1, y2 = cy, cy + height
            z1, z2 = cz - half_d, cz + half_d

            self.player.active_hitbox = (x1, y1, z1, x2, y2, z2)
        else:
            self.player.active_hitbox = None

        if self.player.frame >= self.player.cols:
            self.player.active_hitbox = None
            self.player.state_machine.cur_state.exit(None)


            held_right = self.player.key_down_states.get(SDLK_RIGHT, False)
            held_left = self.player.key_down_states.get(SDLK_LEFT, False)
            held_ctrl = self.player.key_down_states.get(SDLK_LCTRL, False)

            if held_right ^ held_left:
                self.player.face_dir = 1 if held_right else -1
                self.player.dir = self.player.face_dir
                ev = make_keydown_event(SDLK_RIGHT if held_right else SDLK_LEFT)

                self.player.state_machine.cur_state = self.player.RUN
                self.player.state_machine.cur_state.enter(ev)
                self.player.state_machine.next_state = self.player.RUN

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
        screen_y = (self.player.z + self.player.y) - camera.bottom # z, y 적용
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
        self.player.hit_list = []
        self.animation_speed_pps = (ACTION_PER_TIME * 1.5) * FRAMES_PER_ACTION
        self.player.frame_width = self.player.image.w // self.player.cols
        self.player.frame_height = self.player.image.h // self.player.rows

        if self.player.face_dir == 1:
            self.player.row_index = 2
        else:
            self.player.row_index = 3

        if self.player.face_dir == 1:
            self.player.hurt_offset_x = -55
        else:
            self.player.hurt_offset_x = -35

        pass

    def exit(self,e):
        self.player.image = self.player.image_motion

        self.player.cols = 13
        self.player.rows = 8
        self.player.frame_width = self.player.image.w // self.player.cols
        self.player.frame_height = self.player.image.h // self.player.rows
        self.player.active_hitbox = None
        pass

    def do(self):
        self.player.frame += self.animation_speed_pps * game_framework.frame_time

        # y(높이)에 중력 적용
        self.player.yv -= GRAVITY_PPS * game_framework.frame_time
        self.player.y += self.player.yv * game_framework.frame_time

        if self.player.move_speed > 0:
            self.player.move_speed -= FRICTION_PPS * game_framework.frame_time
            if self.player.move_speed < 0:
                self.player.move_speed = 0
        self.player.x += self.player.face_dir * self.player.move_speed * game_framework.frame_time
        if self.player.face_dir == 1:
            self.hitbox_data = (self.player.hurt_offset_x+30, 0, 250, 300, 40)
        else:
            self.hitbox_data = (-self.player.hurt_offset_x+30, 0, 250, 300, 40)

        data = self.hitbox_data
        if data and (self.player.frame > 2.0 and self.player.frame < self.player.cols - 2.0):
            offset_x_rel, offset_z, width, height, depth = data
            offset_x = offset_x_rel * self.player.face_dir

            cx = self.player.x + offset_x
            cy = self.player.y -150
            cz = self.player.z + offset_z
            half_w, half_d = width / 2, depth / 2

            x1, x2 = cx - half_w, cx + half_w
            y1, y2 = cy, cy + height
            z1, z2 = cz - half_d, cz + half_d
            self.player.active_hitbox = (x1, y1, z1, x2, y2, z2)
        else:
            self.player.active_hitbox = None
        # 땅 착지(y=0) 판정
        if self.player.y <= 0:
            self.player.y = 0
            self.player.yv = 0
            self.player.active_hitbox = None

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
        screen_y = (self.player.z + self.player.y) - camera.bottom # z, y 적용

        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height

        self.player.image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                                    screen_x, screen_y, 400, 300)
        pass