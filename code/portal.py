from pico2d import *
# game_framework가 update에서 사용되므로 임포트가 필요합니다.
from code import game_framework

from code.player_about.player_base import * # (사용자 환경에 맞게 유지)

# (가정) 상수가 정의되어 있지 않다면 아래와 같이 정의가 필요합니다.
# 이미 import한 파일에 있다면 주석 처리하세요.
ACTION_PER_TIME = 1.0
FRAMES_PER_ACTION = 8


class Portal:
    image = None

    def __init__(self, x, z, next_stage_name):
        self.x = x
        self.z = z
        self.y = 0  # 포털은 보통 바닥에 위치
        self.next_stage_name = next_stage_name
        self.row_index = 0  # 애니메이션 행 인덱스
        if Portal.image is None:
            # 경로가 맞는지 확인해주세요.
            Portal.image = load_image('sprite/map/portal.png')

            # 충돌 박스 (히트박스) 설정
        self.hurt_w = 100
        self.hurt_h = 250
        self.hurt_d = 50

        # 애니메이션 설정
        self.cols = 1
        self.rows = 5
        self.frame = 0
        self.frame_width = self.image.w // self.cols
        self.frame_height = self.image.h // self.rows

        # 애니메이션 속도
        self.animation_speed_pps = 10.0  # 초당 프레임 재생 속도 (적절히 조절)

    def get_bb_3d(self):
        # 3D AABB 충돌 박스 리턴 (Left, Bottom, Back, Right, Top, Front)
        cx, cy, cz = self.x, self.y, self.z
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
        sx = 0
        self.row_index = int(self.frame)
        sy = (self.rows - 1 - self.row_index) * self.frame_height

        screen_x = self.x - camera.left
        screen_y = (self.z + self.y) - camera.bottom


        self.image.clip_draw(
            sx, 0,  # 잘라낼 이미지의 시작 좌표 (left, bottom)
            self.frame_width,  # 잘라낼 폭
            self.frame_height,  # 잘라낼 높이
            screen_x,  # 화면에 그릴 위치 X
            screen_y  # 화면에 그릴 위치 Y
        )

        # 디버그용 박스 그리기 (draw_3d_box 함수가 정의되어 있다고 가정)
        # hurtbox = self.get_bb_3d()
        # draw_3d_box(self, hurtbox, camera)