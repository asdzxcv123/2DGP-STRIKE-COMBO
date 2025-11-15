from code.dummy import DummyObject
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

        # 프레임 크기 계산
        self.frame_width = self.image.w // self.cols
        self.frame_height = self.image.h // self.rows

        self.last_speed = 0
        self.move_speed = 0
        self.yv = 0 # y(높이) 속도
        self.ground_z = self.z # y -> z
        self.key_down_states={}

        self.combo_stage = 0
        self.last_attack_time = 0.0
        self.afterimages = []

        self.active_hitbox = None
        self.show_hitboxes = False
        self.hurt_w = self.frame_width * 0.20
        self.hurt_h = self.frame_height * 0.5
        if self.face_dir==1:
            self.hurt_offset_x = -50

        self.hurt_offset_y = -self.frame_height * 0.4  # 몸통이 약간 아래쪽
        self.hurt_offset_z = 0  # 발 중심 그대로

        self.draw_w = 400
        self.draw_h = 300

        self.scale_x = self.draw_w / self.frame_width
        self.scale_y = self.draw_h / self.frame_height

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

    def get_bb_3d(self):
        cx = self.x + self.hurt_offset_x
        cy = self.y + self.hurt_offset_y
        cz = self.z + self.hurt_offset_z

        half_w = self.hurt_w / 2
        half_h = self.hurt_h / 2
        half_d = 15  # 라인 여유 폭 (벨트스크롤 핵심)

        x1 = cx - half_w
        x2 = cx + half_w
        y1 = cy
        y2 = cy + self.hurt_h
        z1 = cz - half_d
        z2 = cz + half_d

        return (x1, y1, z1, x2, y2, z2)

    def update(self):
        self.state_machine.update()
        update_afterimages(self, game_framework.frame_time)

        my_hurtbox = self.get_bb_3d()

        #print(f"MY_HURTBOX_DATA: {my_hurtbox}")
        if self.active_hitbox:


            for o in game_world.world[1]:

                if isinstance(o, DummyObject):

                    dummy_hurtbox = o.get_bb_3d()


                    if check_collision_3d(self.active_hitbox, dummy_hurtbox):
                        print("!!! HIT!!! (히트박스 충돌 성공)")
                        pass
        pass

    def draw(self,camera):
        draw_afterimages(self,camera)
        self.state_machine.draw(camera)
        if self.show_hitboxes:
            # 플레이어의 허트박스 (녹색)
            hurtbox = self.get_bb_3d()

            draw_3d_box(self,hurtbox, camera)  # 초록색, 반투명

            # 활성화된 공격 히트박스 (빨간색)
            if self.active_hitbox:

                draw_3d_box(self,self.active_hitbox, camera)  # 빨간색, 반투명

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

        if H_down(('INPUT', event)):
            self.show_hitboxes = not self.show_hitboxes  # 토글
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

