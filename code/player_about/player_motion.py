from code.player_about.player_base import *


class Idle:
    def __init__(self, Player):
        self.player = Player
        pass

    def enter(self, e):
        if self.player.face_dir == -1:
            self.player.row_index = 1
        else:
            self.player.row_index = 0
        self.player.cols = 13
        self.dir = 0
        self.player.ground_z = self.player.z  # y -> z
        self.player.y = 0  # 높이 0
        self.player.yv = 0  # 높이 속도 0
        self.player.move_speed = 0
        pass

    def exit(self, e):
        self.player.last_speed = self.player.move_speed
        pass

    def do(self):
        self.player.frame = (self.player.frame + (
                    ACTION_PER_TIME / 2) * FRAMES_PER_ACTION * game_framework.frame_time) % self.player.cols
        pass

    def draw(self, camera):
        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        if self.player.face_dir == 1:
            self.player.row_index = 0
        else:
            self.player.row_index = 1

        screen_x = self.player.x - camera.left
        # [수정] (z - y) -> (z + y)
        screen_y = (self.player.z + self.player.y) - camera.bottom

        self.player.image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                                    screen_x, screen_y, 400, 300)

class Walk:
    def __init__(self, Player):
        self.player = Player
        self.keydown_time = 0
        pass

    def enter(self, e):
        if self.player.face_dir == 1:
            self.player.row_index = 2
        else:
            self.player.row_index = 3
        self.player.cols = 10

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
                ACTION_PER_TIME * 1.5) * FRAMES_PER_ACTION * game_framework.frame_time) % self.player.cols

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

        z_dir = 0  # y_dir -> z_dir
        if held_up:
            z_dir += 1
        if held_down:
            z_dir -= 1
        # self.player.y -> self.player.z (깊이 이동)
        self.player.z += (WALK_SPEED_PPS * 0.7) * game_framework.frame_time * z_dir

        if not (held_right or held_left or held_up or held_down):
            self.player.state_machine.cur_state.exit(None)
            self.player.state_machine.cur_state = self.player.IDLE
            self.player.state_machine.cur_state.enter(None)
        elif (held_up and held_down) and (x_dir == 0):
            self.player.state_machine.cur_state.exit(None)
            self.player.state_machine.cur_state = self.player.IDLE
            self.player.state_machine.cur_state.enter(None)
        pass

    def draw(self, camera):
        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        if self.player.face_dir == 1:
            self.player.row_index = 2
        else:
            self.player.row_index = 3
        screen_x = self.player.x - camera.left
        screen_y = (self.player.z - self.player.y) - camera.bottom  # z, y 적용
        self.player.image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                                    screen_x, screen_y, 400, 300)


class Run:
    def __init__(self, Player):
        self.player = Player
        pass

    def enter(self, e):
        if self.player.face_dir == 1:
            self.player.row_index = 4
        else:
            self.player.row_index = 5
        self.player.cols = 7

        self.player.move_speed = RUN_SPEED_PPS
        pass

    def exit(self, e):
        self.player.last_speed = self.player.move_speed
        pass

    def do(self):
        self.player.frame = (self.player.frame + (
                ACTION_PER_TIME * 1.3) * FRAMES_PER_ACTION * game_framework.frame_time) % self.player.cols

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
        self.player.x += x_dir * RUN_SPEED_PPS * game_framework.frame_time
        z_dir = 0  # y_dir -> z_dir
        if held_up:
            z_dir += 1
        if held_down:
            z_dir -= 1
        self.player.z += (WALK_SPEED_PPS * 0.3) * game_framework.frame_time * z_dir  # y -> z
        self.player.move_speed = RUN_SPEED_PPS
        self.player.last_move_speed = self.player.move_speed

        z_dir = 0  # y_dir -> z_dir
        if self.player.key_down_states.get(SDLK_UP, False):
            z_dir += 1
        if self.player.key_down_states.get(SDLK_DOWN, False):
            z_dir -= 1
        self.player.z += (WALK_SPEED_PPS * 0.4) * game_framework.frame_time * z_dir  # y -> z

        pass

    def draw(self, camera):
        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        if self.player.face_dir == 1:
            self.player.row_index = 4
        else:
            self.player.row_index = 5
        screen_x = self.player.x - camera.left
        # [수정] (z - y) -> (z + y)
        screen_y = (self.player.z + self.player.y) - camera.bottom
        self.player.image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                                    screen_x, screen_y, 400, 300)
        pass

class Jump:
    def __init__(self, Player):
        self.player = Player

        pass

    def enter(self, e):
        self.player.cols = 5
        held_up = self.player.key_down_states.get(SDLK_UP, False)
        held_down = self.player.key_down_states.get(SDLK_DOWN, False)
        held_right = self.player.key_down_states.get(SDLK_RIGHT, False)
        held_left = self.player.key_down_states.get(SDLK_LEFT, False)
        if (held_up ^ held_down) and (not held_left ^ held_right):
            self.player.last_speed = 0
        self.player.move_speed = self.player.last_speed
        if self.player.face_dir == 1:
            self.player.row_index = 6
        else:
            self.player.row_index = 7

        if self.player.yv == 0:
            self.player.yv = JUMP_VELOCITY_PPS
        self.event = None
        pass

    def exit(self, e):
        self.event = None
        pass

    def do(self):
        # [수정] (cols-1) -> cols, 애니메이션이 마지막 프레임까지 돌도록
        self.player.frame = (self.player.frame + (
            ACTION_PER_TIME) * FRAMES_PER_ACTION * game_framework.frame_time) % self.player.cols

        self.player.yv -= GRAVITY_PPS * game_framework.frame_time
        self.player.y += self.player.yv * game_framework.frame_time

        if self.player.move_speed > 0:
            self.player.move_speed -= FRICTION_PPS * game_framework.frame_time

            if self.player.move_speed < 0:
                self.player.move_speed = 0

        self.player.x += self.player.face_dir * self.player.move_speed * game_framework.frame_time

        if self.player.y <= 0:
            self.player.y = 0
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

    def draw(self, camera):
        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height
        if self.player.face_dir == 1:
            self.player.row_index = 6
        else:
            self.player.row_index = 7
        screen_x = self.player.x - camera.left
        # [수정] (z - y) -> (z + y)
        screen_y = (self.player.z + self.player.y) - camera.bottom

        self.player.image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                                    screen_x, screen_y, 400, 300)
        pass