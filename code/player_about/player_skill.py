from code.player_about.player_base import *

class Skill_Bash:
    def __init__(self, Player):
        self.player=Player
        self.fire_c=0
        pass

    def enter(self, e):
        self.player.image = self.player.image_bash
        self.player.frame = 0
        self.fire_c = 0
        self.player.rows = 2
        self.player.cols = 6

        self.animation_speed_pps = (ACTION_PER_TIME * 1.5) * FRAMES_PER_ACTION
        self.player.frame_width = self.player.image.w // self.player.cols
        self.player.frame_height = self.player.image.h // self.player.rows
        pass

    def exit(self,e=None):
        self.player.image = self.player.image_motion

        self.player.cols = 13
        self.player.rows = 8
        self.player.frame_width = self.player.image.w // self.player.cols
        self.player.frame_height = self.player.image.h // self.player.rows
        pass

    def do(self):
        self.player.frame += self.animation_speed_pps * game_framework.frame_time

        if self.player.frame >= self.player.cols-3:
            if self.fire_c==0:
                self.player.fire_sword()
                self.fire_c=1
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

        screen_x = self.player.x - camera.left
        screen_y = self.player.y - camera.bottom

        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height

        self.player.image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                                    screen_x, screen_y, 400, 300)
        pass


class Dash:
    def __init__(self, Player):
        self.player = Player
        self.DASH_SPEED_PPS = RUN_SPEED_PPS * 2.5
        self.animation_speed_pps = 0.0

        self.afterimage_timer = 0.0
        self.AFTERIMAGE_SPAWN_INTERVAL = 0.08
        pass


    def enter(self, e):
        self.player.image=self.player.image_dash
        self.player.frame = 0
        self.player.cols=8
        self.player.rows=2

        self.player.frame_width = self.player.image.w // self.player.cols
        self.player.frame_height = self.player.image.h // self.player.rows

        self.animation_duration = 0.3
        #self.animation_speed_pps = self.player.cols / self.animation_duration
        self.animation_speed_pps = (ACTION_PER_TIME * 2.0) * FRAMES_PER_ACTION

        self.afterimage_timer = 0.0

        pass

    def exit(self,e=None):
        self.player.image = self.player.image_motion

        self.player.cols = 13
        self.player.rows = 8
        self.player.frame_width = self.player.image.w // self.player.cols
        self.player.frame_height = self.player.image.h // self.player.rows
        pass

    def do(self):
        self.player.frame += self.animation_speed_pps * game_framework.frame_time
        self.player.x += self.DASH_SPEED_PPS * self.player.face_dir * game_framework.frame_time

        self.afterimage_timer += game_framework.frame_time
        if self.afterimage_timer >= self.AFTERIMAGE_SPAWN_INTERVAL:
            add_afterimage(self.player, self.player.image_dash)
            self.afterimage_timer -= self.AFTERIMAGE_SPAWN_INTERVAL
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

    def draw(self, camera):
        if self.player.face_dir == 1:
            self.player.row_index = 0  # 0번 줄: 오른쪽 대쉬
        else:
            self.player.row_index = 1  # 1번 줄: 왼쪽 대쉬

        screen_x = self.player.x - camera.left
        screen_y = self.player.y - camera.bottom

        sx = int(self.player.frame) * self.player.frame_width
        sy = (self.player.rows - 1 - self.player.row_index) * self.player.frame_height

        self.player.image.clip_draw(sx, sy, self.player.frame_width, self.player.frame_height,
                                    screen_x, screen_y, 400, 300)

        pass
