from pico2d import *
from code.player_about.player_base import draw_3d_box


class DummyObject:
    def __init__(self, x, z):
        self.x = x
        self.z = z
        self.y = 0  # 높이

        # 플레이어 이미지를 재활용 (테스트용)
        # 나중에 허수아비 이미지로 바꾸셔도 됩니다.
        self.image = load_image('sprite/player/player_motion.png')
        self.frame = 0
        self.row_index = 0  # 가만히 서 있는 모션

        self.cols = 13
        self.rows = 8
        self.frame_width = self.image.w // self.cols
        self.frame_height = self.image.h // self.rows

        # 그리기 크기 (draw_3d_box가 참조)
        self.draw_w = 400
        self.draw_h = 300
        self.scale_x = self.draw_w / self.frame_width
        self.scale_y = self.draw_h / self.frame_height

        # --- 허트박스 (피격 판정) ---
        self.hurt_w = self.frame_width * 0.20
        self.hurt_h = self.frame_height * 0.5
        self.hurt_d = 30  # 깊이 (z1 ~ z2)


        self.hurt_offset_x = -50

        self.hurt_offset_y = -self.frame_height * 0.4
        self.hurt_offset_z = 0

    # 플레이어와 동일한 인터페이스
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

    def update(self):
        # 지금은 아무것도 안 함
        pass

    def draw(self, camera):
        # 1. 스프라이트 그리기
        screen_x = self.x - camera.left
        screen_y = (self.z + self.y) - camera.bottom

        sx = int(self.frame) * self.frame_width
        sy = (self.rows - 1 - self.row_index) * self.frame_height

        self.image.clip_draw(sx, sy, self.frame_width, self.frame_height,
                             screen_x, screen_y, self.draw_w, self.draw_h)

        # 2. 허트박스 그리기 (파란색)
        hurtbox = self.get_bb_3d()
        draw_3d_box(self, hurtbox, camera)
