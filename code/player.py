from code.player_about.player_motion import *
from code.player_about.player_attack import *
from code.player_about.player_skill import *





class Player:
    Image = None
    def __init__(self):
        self.image_motion = load_image('sprite/player/player_motion.png')
        self.image_attack = load_image('sprite/player/player_attack.png')
        self.image_MtoA=load_image('sprite/player/motion_attack.png')
        self.image_bash=load_image('sprite/player/bash_skill.png')
        self.image_dash=load_image('sprite/player/Dash.png')
        self.image = self.image_motion
        self.landing_lock = False
        self.wait_neutral = False

        self.x = 400
        self.z = 300  # y -> z (깊이)
        self.y = 0    # y (높이)
        self.frame = 0
        self.face_dir=1
        self.dir=0
        self.y_dir=0
        self.cols = 13
        self.rows = 8
        self.row_index = 0

        self.last_speed = 0
        self.move_speed = 0
        self.yv = 0 # y(높이) 속도
        self.ground_z = self.z # y -> z
        self.key_down_states={}

        self.combo_stage = 0
        self.last_attack_time = 0.0
        self.afterimages = []

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
        self.BASH_SKILL=Skill_Bash(self)
        self.DASH=Dash(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.WALK, left_down: self.WALK,
                            up_down: self.WALK, down_down:self.WALK,
                            C_down: self.JUMP, X_down: self.ATTACK,
                            Q_down: self.BASH_SKILL, Shift_down:self.DASH},
                self.WALK: {L_ctrl_down: self.RUN,C_down: self.JUMP,
                            X_down: self.ATTACK, Q_down: self.BASH_SKILL},
                self.RUN: {right_down: self.IDLE, left_down: self.IDLE, right_up: self.IDLE, left_up: self.IDLE,
                           C_down: self.JUMP, X_down: self.RUN_ATTACK,
                           Q_down: self.BASH_SKILL},
                self.JUMP:{X_down:self.JUMP_ATTACK},
                self.ATTACK:{},
                self.RUN_ATTACK:{},
                self.JUMP_ATTACK:{},
                self.BASH_SKILL:{},
                self.DASH:{}
            }
        )
        self.landing_lock_until = 0.0

    def update(self):
        self.state_machine.update()
        update_afterimages(self, game_framework.frame_time)
        pass

    def draw(self,camera):
        draw_afterimages(self,camera)
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
    def fire_sword(self):
        if(self.face_dir==1):
            spawn_x=self.x+(5*self.face_dir)
        else:
            spawn_x = self.x + (100 * self.face_dir)
        # y -> z, y (z, y 좌표 전달)
        fire_aura=SwordP(spawn_x, self.z, self.y, self.face_dir)
        game_world.add_object(fire_aura,1)