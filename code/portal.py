from pico2d import *
from code import game_framework
from code.player_about.player_base import draw_3d_box


class Portal:
    image = None

    def __init__(self, x, z, next_stage_name):

        self.x = x
        self.z = z
        self.y = 0
        self.next_stage_name = next_stage_name

        if Portal.image is None:
            Portal.image = load_image('sprite/map/portal.png')

        # [핵심 수정 1] 허트박스 크기를 이미지 그리기 크기(200x200)에 맞춰 확장
        # 이렇게 해야 눈에 보이는 포탈 그림 전체가 감지 영역이 됩니다.
        self.hurt_w = 180  # 너비 (이미지 200보다 약간 작게)
        self.hurt_h = 250  # 높이 (플레이어 키 고려)

        # [핵심 수정 2] 깊이(Z축)를 대폭 늘림 (기존 80 -> 150)
        # 화면상에서 포탈의 위/아래 부분(Z축 깊이)을 밟아도 인식되도록 합니다.
        self.hurt_d = 30
        self.hurt_offset_x = 0
        self.hurt_offset_y =0
        self.hurt_offset_z = -30
        # 애니메이션 설정
        self.cols = 1
        self.rows = 5
        self.frame = 0
        self.frame_width = self.image.w // self.cols
        self.frame_height = self.image.h // self.rows
        self.animation_speed_pps = 10.0

    def get_bb_3d(self):

        cx= self.x+self.hurt_offset_x
        cy=self.y+self.hurt_offset_y
        cz=self.z+self.hurt_offset_z
        half_w, half_d = self.hurt_w / 2, self.hurt_d / 2

        x1 = cx - half_w
        x2 = cx + half_w
        y1 = cy
        y2 = cy + self.hurt_h
        z1 = cz - half_d
        z2 = cz + half_d
        return (x1, y1, z1, x2, y2, z2)

    def update(self):
        self.frame = (self.frame + self.animation_speed_pps * game_framework.frame_time) % self.rows

    def draw(self, camera):
        self.row_index = int(self.frame)

        # 이미지 그리기 (중심 기준)
        screen_x = self.x - camera.left
        screen_y = (self.z + self.y) - camera.bottom

        # [참고] 여기서 200, 200 크기로 그리므로, 위에서 hurt_w, hurt_d를 이에 맞춰 키웠습니다.
        self.image.clip_draw(0, 0,self.frame_width, self.frame_height,screen_x, screen_y,200, 200)

        # 디버그용 박스 (H키 눌러서 확인 시 이제 이미지 크기와 비슷하게 보일 것입니다)
        hurtbox = self.get_bb_3d()
        draw_3d_box(self, hurtbox, camera)