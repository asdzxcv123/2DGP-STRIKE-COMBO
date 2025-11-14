from code.player_about.player_base import *


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
